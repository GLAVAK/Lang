package com.emeraldpowder.Preprocessor;

import com.emeraldpowder.Common.PositionInCode;

/**
 * Created by glavak on Feb 16, 17.
 */
public class CodeBlockEmpty extends CodeBlock
{
    public CodeBlockEmpty(PositionInCode positionInCode)
    {
        super(positionInCode);
    }

    @Override
    PositionInCode getArrowPosition()
    {
        return position;
    }
}
