# API Documenttion
- [Authentication](#authentication)


<a name="authentication"></a>

## Authentication
The authentication is based on [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

**Request**
|Type|Path|
|--|--|
|POST|/api/accounts/get_token|

**Header**
|Key|Value|
|--|--|
|Content-Type|application/json|

**Get data**
No Get Properties possible / required

**Post data**
|key|type|required|description|
|--|--|--|--|
|email|string|true|Users Email Address|
|password|string|true|Users Password|

**Possible Response Status**
|Code|Message|Description|
|--|--|--|
| 200 | OK | Login was successfull |
| 401 | Unauthorized | Email or password was wrong |
| 400 | Bad Request | Missing Property |

**Successfull Response Example**
```
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNTgzNDM1MywianRpIjoiZGY3OGJkNDRiMmQyNDQ3NGE4MzYwZTdmYTQ2M2VkNjciLCJ1c2VyX2lkIjoxfQ.Yd89rUBaWAGgVgdH2lo_vsB2i7utQTZXYgtQ7SN4UR8",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE1NzQ4MjUzLCJqdGkiOiJmZWE4NjVhZmU2Yzk0OWUzYjg0Y2JkZTUxZGUzMzViOCIsInVzZXJfaWQiOjF9._18WMTBfxFTlojV25Ogr1aHAjiWZiSfgHC6WWXI9rAY"
}
```

We are not working with refresh key currently. The User will be identified by `access` property.