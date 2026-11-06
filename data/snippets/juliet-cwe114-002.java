    private void handleRequest() throws Throwable
    {

        String root;
        String libraryName = "test.dll";

        if(System.getProperty("os.name").toLowerCase().indexOf("win") >= 0)
        {
            root = "C:\\libs\\";
        }
        else
        {
            root = "/home/user/libs/";
        }

        System.load(root + libraryName);

    }
