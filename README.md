The exploit is a python script for the new TryHackme room "capturereturns". Like the previous room named "capture", you need to bruteforce a login page while solving CAPTCHA. The trick here is that
we need to use libraries for OCR(optical character recognition) in order to extract the text from the images and solve the CAPTCHA. But because we depend on the response of the server to recognize 
the CAPTCHA or the invalid logins, and after a lot of thought, I thought about checking whether the response would be equal to "THM" or not, so the login would be successful and break the execution of the
bruteforcing.
