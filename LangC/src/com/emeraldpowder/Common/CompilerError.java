package com.emeraldpowder.Common;

/**
 * Created by glavak on Feb 16, 17.
 */
public class CompilerError extends Exception
{
    public PositionInCode positionInCode;

    public CompilerError(PositionInCode positionInCode, String message, Object... args)
    {
        super(String.format(message, args));
        this.positionInCode = positionInCode;
    }

    public CompilerError(PositionInCode positionInCode, String message)
    {
        super(message);
        this.positionInCode = positionInCode;
    }

    @Override
    public String toString()
    {
        return String.format(
                "(%d:%d-%d): %s",
                positionInCode.getLine() + 1,
                positionInCode.getColumn() + 1,
                positionInCode.getRightColumn() + 1,
                getMessage());
    }
}
