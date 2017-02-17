package com.emeraldpowder.Preprocessor;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

/**
 * Created by glavak on Feb 16, 17.
 */
class Utils
{
    private static final Set<Character> spaces = new HashSet<>(Arrays.asList(
            new Character[]{' ', '-', '+', '|'}
    ));

    static boolean isSpace(char c)
    {
        return spaces.contains(c);
    }

    static MovingDirection charToDirection(char c)
    {
        switch (c)
        {
            case '^':
                return MovingDirection.Up;
            case '>':
                return MovingDirection.Right;
            case 'v':
                return MovingDirection.Down;
            case '<':
                return MovingDirection.Left;
            default:
                return null;
        }
    }
}
