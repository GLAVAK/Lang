package com.emeraldpowder.Preprocessor;

import com.emeraldpowder.Common.PositionInCode;

/**
 * Created by glavak on 17.02.17.
 */
public class Token
{
    public PositionInCode position;
    public String content = "";

    public Token(PositionInCode position, String content)
    {
        this.position = position;
        this.content = content;
    }
}
