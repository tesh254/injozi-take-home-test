# injozi-take-home-test

## Setup locally
- Create new `.env` from `.env.example`
- Create virtual environment
```bash
python3 -m virtualenv venv
```
- Activate environment
```bash
source venv/bin/activate
```
- Run server
```
python app.py
```

## Endpoints
### Login

`/api/v1/login`

```bash
Request Body:
{
    "email": string;
    "password": string;
}
```

Reponse: `200 OK`

```json
{
  "access_token": "sometoken"
}
```

### Register

`/api/v1/register`

Request Body:

```bash
    {
        "email": string;
        "password": string;
        "name"?: string;
        "surname"?: string;
        "phone"?: string;
    }
```

Response `201 Created`

```json
{
  "user": {
    "email": "test@gmail.com"
  },
  "access_token": "yourauthtoken"
}
```

### Profile

`/api/v1/profile`
Request Header:

```bash
Authorization: Bearer <yourauthtoken>
```

Response `200 OK`

```json
{
  "name": "your name",
  "surname": "your surname",
  "email": "your email",
  "phone": "your phone"
}
```

### List Profiles

`/api/v1/profiles`

Response `200 OK`

```json
{
  "profile": [
    {
      "name": "your name",
      "surname": "your surname",
      "email": "your email",
      "phone": "your phone"
    }
  ]
}
```
