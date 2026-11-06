    public void handleRequest() throws Throwable
    {
        byte data;

        data = 2;

        if(data < 0)
        {
            byte result = (byte)(data * 2);
            IO.writeLine("result: " + result);
        }

    }
