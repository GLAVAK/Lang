package com.emeraldpowder.Common;

/**
 * Created by glavak on Feb 16, 17.
 */
public class InternalError extends Exception
{
    public InternalError(String message, Object... args)
    {
        super(String.format(message, args));
    }

    public InternalError(String message)
    {
        super(message);
    }
}
