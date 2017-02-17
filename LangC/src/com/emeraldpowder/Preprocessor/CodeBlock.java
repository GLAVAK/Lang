package com.emeraldpowder.Preprocessor;

import com.emeraldpowder.Common.PositionInCode;

/**
 * Created by glavak on Feb 16, 17.
 */
public abstract class CodeBlock
{
    public PositionInCode position;
    public CodeBlock nextBlock;
    public String content;

    MovingDirection arrowDirection;

    public CodeBlock(PositionInCode position)
    {
        this.position = position;
    }

    abstract PositionInCode getArrowPosition();
}
