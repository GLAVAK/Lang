package com.emeraldpowder.Preprocessor;

import com.emeraldpowder.Common.CompilerError;
import com.emeraldpowder.Common.PositionInCode;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

/**
 * Created by glavak on 17.02.17.
 */
class BlockContentParser
{
    private static boolean isLetter(char c)
    {
        return (c >= 'a' && c <= 'z') ||
                (c >= 'A' && c <= 'Z') ||
                (c >= '0' && c <= '9');
    }

    private static final Set<Character> symbols = new HashSet<>(Arrays.asList(
            new Character[]{'+', '-', '*', '/', '(', ')', '=', '<', '>', '|', '&'}
    ));

    private static boolean isSymbol(char c)
    {
        return symbols.contains(c);
    }

    private static boolean isSpace(char c)
    {
        return c == ' ';
    }

    static ArrayList<Token> stringToTokens(String string, PositionInCode startingPosition) throws CompilerError
    {
        ArrayList<Token> result = new ArrayList<>();

        Token currentToken = null;

        for (int i = 0; i < string.length(); i++)
        {
            char currentChar = string.charAt(i);
            PositionInCode currentPosition = new PositionInCode(
                    startingPosition.getLine(),
                    startingPosition.getColumn() + i);

            if (currentToken == null)
            {
                if (isSpace(currentChar))
                {
                    continue;
                }
                else if (isSymbol(currentChar) || isLetter(currentChar))
                {
                    currentToken = new Token(currentPosition, currentChar + "");
                    result.add(currentToken);
                }
                else
                {
                    throw new CompilerError(currentPosition, "Invalid token '%s'", currentChar + "");
                }
            }
            else
            {
                if (isSpace(currentChar))
                {
                    currentToken.position.setWidth(i - currentToken.position.getColumn());
                    currentToken = null;
                }
                else if ((isSymbol(currentChar) && isLetter(currentToken.content.charAt(0))) ||
                        (isLetter(currentChar) && isSymbol(currentToken.content.charAt(0))))
                {
                    currentToken.position.setWidth(i - currentToken.position.getColumn());
                    currentToken = new Token(currentPosition, currentChar + "");
                    result.add(currentToken);
                }
                else if ((isSymbol(currentChar) && isSymbol(currentToken.content.charAt(0))) ||
                        (isLetter(currentChar) && isLetter(currentToken.content.charAt(0))))
                {
                    currentToken.content += currentChar;
                }
                else
                {
                    throw new CompilerError(currentPosition, "Invalid token '%s'", currentChar + "");
                }
            }
        }

        return result;
    }
}
