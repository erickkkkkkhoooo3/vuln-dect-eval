    public void handleRequest(HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        String data;

        data = "foo";

        if (data != null)
        {
            Cookie cookieSink = new Cookie("lang", data);
            response.addCookie(cookieSink);
        }

    }
