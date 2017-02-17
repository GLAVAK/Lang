package com.emeraldpowder.Common;

/**
 * Created by glavak on Feb 16, 17.
 */
public class PositionInCode
{
    private int line;
    private int column;
    private int width;

    public int getLine()
    {
        return line;
    }

    public void setLine(int line)
    {
        this.line = line;
    }

    public int getColumn()
    {
        return column;
    }

    public int getRightColumn()
    {
        return column + width - 1;
    }

    public void setColumn(int column)
    {
        this.column = column;
    }

    public int getWidth()
    {
        return width;
    }

    public void setWidth(int width)
    {
        this.width = width;
    }

    public PositionInCode()
    {
        this.width = 1;
    }

    public PositionInCode(int line, int column)
    {
        this.line = line;
        this.column = column;
        this.width = 1;
    }

    public PositionInCode(int line, int column, int width)
    {
        this.line = line;
        this.column = column;
        this.width = width;
    }
}