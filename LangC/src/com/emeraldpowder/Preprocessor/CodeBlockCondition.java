package com.emeraldpowder.Preprocessor;

import com.emeraldpowder.Common.PositionInCode;

/**
 * Created by glavak on Feb 16, 17.
 */
public class CodeBlockCondition extends CodeBlock
{
    public CodeBlock nextElseBlock;

    MovingDirection arrowElseDirection;

    public CodeBlockCondition(PositionInCode positionInCode)
    {
        super(positionInCode);
    }

    @Override
    PositionInCode getArrowPosition()
    {
        return new PositionInCode(position.getLine(), position.getRightColumn());
    }

    PositionInCode getElseArrowPosition()
    {
        return position;
    }
}
