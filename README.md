# website_error_checking_tool

![Error Checker Tool](screenshots/1)

You can enter any website url to check the entire page and its sub navigating links. 

![Error Checker Tool](screenshots/2)

It will start to scan and show scanning progress real-time using **StreamingHttpResponse**

![Error Checker Tool](screenshots/4)

Once the check completed it will list out the error code. In this case its **404**. Which means **Not Found**

**Note** In my project the system only check for **404** Not found error. If you want to add further error codes like **400, 401, 402, 403** etc. Add your desired error code in the list variable `error_codes` located on `app.py`. 

Example:
`error_codes = [404, 400, 401, 402, 403]`

The error code will also save to MongoDB along with its URL. The sample schema is added in below image.

![Error Checker Tool](screenshots/3)
