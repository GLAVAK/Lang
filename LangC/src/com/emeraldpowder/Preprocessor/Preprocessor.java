package com.emeraldpowder.Preprocessor;

import com.emeraldpowder.Common.CompilerError;
import com.emeraldpowder.Common.InternalError;
import com.emeraldpowder.Common.PositionInCode;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Created by glavak on Feb 16, 17.
 */

public class Preprocessor
{
    private CodeBlock startingBlock;
    private ArrayList<CodeBlock> blocks;

    public CodeBlock getStartingBlock()
    {
        return startingBlock;
    }

    public ArrayList<CodeBlock> getBlocks()
    {
        return blocks;
    }

    private BufferedReader codeReader;

    public Preprocessor(BufferedReader codeReader)
    {
        this.codeReader = codeReader;
    }

    public void readBlocks()
            throws IOException, CompilerError
    {
        this.blocks = new ArrayList<>();

        for (int i = 0; ; i++)
        {
            String line = codeReader.readLine();
            if (line == null) break;
            parseLine(line, i);
        }
    }

    private void parseLine(String line, int lineNum)
            throws CompilerError
    {
        CodeBlock currentBlock = null;

        for (int i = 0; i < line.length(); i++)
        {
            char currentChar = line.charAt(i);

            if (currentBlock != null)
            {
                if ((currentBlock instanceof CodeBlockStatement && currentChar == ']') ||
                        (currentBlock instanceof CodeBlockCondition && currentChar == '}'))
                {
                    // End of block
                    endBlock(line, i, currentBlock);
                    currentBlock = null;
                }
            }
            else
            {
                MovingDirection currentCharDirection = Utils.charToDirection(currentChar);

                if (currentCharDirection != null &&
                        (i + 1 == line.length() || Utils.isSpace(line.charAt(i + 1))))
                {
                    // Just an empty block
                    CodeBlockEmpty block = new CodeBlockEmpty(new PositionInCode(lineNum, i));
                    block.arrowDirection = currentCharDirection;
                    blocks.add(block);
                }
                else if (currentChar == '[')
                {
                    // Beginning of statement block
                    currentBlock = new CodeBlockStatement(new PositionInCode(lineNum, i));
                }
                else if (currentChar == '{')
                {
                    // Beginning of condition block
                    currentBlock = new CodeBlockCondition(new PositionInCode(lineNum, i));
                }
                else if (currentCharDirection == null && !Utils.isSpace(currentChar))
                {
                    throw new CompilerError(
                            new PositionInCode(lineNum, i),
                            "Invalid token %s", currentChar);
                }
            }
        }
    }

    private void endBlock(String line, int columnNum, CodeBlock currentBlock)
            throws CompilerError
    {
        currentBlock.content= line.substring(currentBlock.position.getColumn()+1, columnNum);

        MovingDirection arrowOnLeft = null;
        MovingDirection arrowOnRight = null;
        if (currentBlock.position.getColumn() > 0)
        {
            char charOnLeft = line.charAt(currentBlock.position.getColumn() -1);
            arrowOnLeft = Utils.charToDirection(charOnLeft);
            currentBlock.position.setColumn(currentBlock.position.getColumn() -1);
        }
        if (columnNum + 1 < line.length())
        {
            char charOnRight = line.charAt(columnNum + 1);
            arrowOnRight = Utils.charToDirection(charOnRight);
        }


        if (currentBlock instanceof CodeBlockStatement)
        {
            currentBlock.position.setWidth(columnNum - currentBlock.position.getColumn() + 2);
            if ((arrowOnLeft == null) == (arrowOnRight == null))
            {
                throw new CompilerError(
                        currentBlock.position,
                        "Statement block should have arrows on only one sides");
            }
            else
            {
                currentBlock.arrowDirection = (arrowOnLeft != null ? arrowOnLeft : arrowOnRight);
            }
        }
        else
        {
            currentBlock.position.setWidth(columnNum - currentBlock.position.getColumn() + 3);
            if (arrowOnLeft == null || arrowOnRight == null)
            {
                throw new CompilerError(
                        currentBlock.position,
                        "Conditional block should have arrows on both sides");
            }
            else
            {
                currentBlock.arrowDirection = arrowOnRight;
                ((CodeBlockCondition)currentBlock).arrowElseDirection = arrowOnLeft;
            }
        }

        blocks.add(currentBlock);
    }

    public void linkBlocks()
            throws CompilerError, InternalError
    {
        if (blocks == null) throw new InternalError("Call to CompileBlocks() before readBlocks()");

        for (CodeBlock block : blocks)
        {
            block.nextBlock = findBlockByArrow(block.getArrowPosition(), block.arrowDirection);
            if (block instanceof CodeBlockCondition)
            {
                CodeBlockCondition blockAsCondition = (CodeBlockCondition)block;
                blockAsCondition.nextElseBlock = findBlockByArrow(
                        blockAsCondition.getElseArrowPosition(),
                        blockAsCondition.arrowElseDirection);
            }
        }
    }

    private CodeBlock findBlockByArrow(PositionInCode arrowPosition, MovingDirection arrowDirection)
    {
        CodeBlock bestFit = null;

        for (CodeBlock block : blocks)
        {
            if (arrowDirection == MovingDirection.Up || arrowDirection == MovingDirection.Down)
            {
                if (arrowPosition.getColumn() < block.position.getColumn() ||
                        block.position.getRightColumn() < arrowPosition.getColumn())
                {
                    continue;
                }

                if (arrowDirection == MovingDirection.Down &&
                        block.position.getLine() > arrowPosition.getLine() &&
                        (bestFit == null || block.position.getLine() < bestFit.position.getLine()))
                {
                    bestFit = block;
                }
                else if (arrowDirection == MovingDirection.Up &&
                        block.position.getLine() < arrowPosition.getLine() &&
                        (bestFit == null || block.position.getLine() > bestFit.position.getLine()))
                {
                    bestFit = block;
                }
            }
            else
            {
                if (block.position.getLine() != arrowPosition.getLine())
                {
                    continue;
                }

                if (arrowDirection == MovingDirection.Right &&
                        block.position.getColumn() > arrowPosition.getColumn() &&
                        (bestFit == null || block.position.getColumn() < bestFit.position.getColumn()))
                {
                    bestFit = block;
                }
                else if (arrowDirection == MovingDirection.Left &&
                        block.position.getColumn() < arrowPosition.getColumn() &&
                        (bestFit == null || block.position.getColumn() > bestFit.position.getColumn()))
                {
                    bestFit = block;
                }
            }
        }

        return bestFit;
    }
}
