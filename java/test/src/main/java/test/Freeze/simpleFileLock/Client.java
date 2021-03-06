// **********************************************************************
//
// Copyright (c) 2003-2018 ZeroC, Inc. All rights reserved.
//
// **********************************************************************

package test.Freeze.simpleFileLock;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Client
{
    private static void
    test(boolean b)
    {
        if(!b)
        {
            throw new RuntimeException();
        }
    }

    public static void
    main(String[] argvs)
    {
        Freeze.FileLock lock = null;

        lock = new Freeze.FileLock("file.lock");
        test(true);

        //
        // Force GC here to ensure that temp references in FileLock
        // are collected and that not affect file locking.
        //
        java.lang.Runtime.getRuntime().gc();

        System.out.println("File lock acquired.");
        System.out.println("Enter some input and press enter, to release the lock and terminate the program.");

        //
        // Block the test waiting for IO, so the file lock is preserved.
        //
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        try
        {
            br.readLine();
        }
        catch(java.io.IOException ex)
        {
            System.out.println("exception:\n " + ex.toString());
            test(false);
        }

        if(lock != null)
        {
            lock.release();
        }
        System.out.println("File lock released.");
    }
}
