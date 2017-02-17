package com.emeraldpowder;

import com.emeraldpowder.Common.CompilerError;
import com.emeraldpowder.Common.InternalError;
import com.emeraldpowder.Preprocessor.Preprocessor;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Main
{
    public static void main(String[] args)
    {
        try
        {
            compileFile("../tests/fibb.txt");
        }
        catch (CompilerError error)
        {
            System.out.println("Compilation aborted due to following error:");
            System.out.println("\t" + error.toString());
        }
        catch (InternalError error)
        {
            System.out.println("Compilation aborted due to internal error, please, contact developer:");
            System.out.println("\t" + error.toString());
        }
        catch (IOException error)
        {
            System.out.println("Error reading file:");
            System.out.println("\t" + error.toString());
        }
    }

    private static void compileFile(String filename)
            throws IOException, CompilerError, InternalError
    {
        FileReader reader = new FileReader(filename);
        Preprocessor preprocessor = new Preprocessor(new BufferedReader(reader));

        preprocessor.readBlocks();
        preprocessor.linkBlocks();
    }
}
