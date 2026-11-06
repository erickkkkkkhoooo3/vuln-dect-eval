    private void handleRequest() throws Throwable
    {

        int[] intArray = new int[10];
        int i = 0;

        do
        {
            IO.writeLine("intArray[" + i + "] = " + (intArray[i] = i));
            i++;
        }
        while (i < intArray.length);

    }
