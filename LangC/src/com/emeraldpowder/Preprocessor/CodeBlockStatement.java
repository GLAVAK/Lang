package com.emeraldpowder.Preprocessor;

import com.emeraldpowder.Common.PositionInCode;

/**
 * Created by glavak on Feb 16, 17.
 */
public class CodeBlockStatement extends CodeBlock
{
    boolean isArrowOnRight;

    public CodeBlockStatement(PositionInCode positionInCode)
    {
        super(positionInCode);
    }

    @Override
    PositionInCode getArrowPosition()
    {
        if (isArrowOnRight)
        {
            return new PositionInCode(position.getLine(), position.getRightColumn());
        }
        else
        {
            return position;
        }
    }
}
