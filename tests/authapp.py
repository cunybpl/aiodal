# only need this to make a mock app for testing aiodal.web.auth

from typing import Dict, Optional
from fastapi import FastAPI, Depends, Security
from fastapi.testclient import TestClient
from pydantic import Field

from aiodal.web.auth import Auth0, Auth0User, security_responses


###############################################################################
class CustomAuth0User(Auth0User):
    grant_type: Optional[str] = Field(None, alias="gty")


###############################################################################
auth = Auth0(domain="domain", api_audience="audience")
auth_custom = Auth0(
    domain="domain", api_audience="audience", user_model=CustomAuth0User
)
auth.jwks = {
    "keys": [
        {
            "kid": "veryrealkid",
            "kty": "veryreal_kty",
            "use": "veryreal_use",
            "n": "veryreal_n",
            "e": "veryreal_e",
        }
    ]
}
auth.algorithms = ["veryfast"]
auth_custom.jwks = {
    "keys": [
        {
            "kid": "veryrealkid",
            "kty": "veryreal_kty",
            "use": "veryreal_use",
            "n": "veryreal_n",
            "e": "veryreal_e",
        }
    ]
}
auth_custom.algorithms = ["veryfast"]
app = FastAPI()


# set ups for testing auth functionality


@app.get("/public")
async def get_public():
    return {"message": "Anonymous user"}


@app.get("/also-public", dependencies=[Depends(auth.implicit_scheme)])
async def get_public2():
    return {
        "message": "Anonymous user (token is received from swagger ui but not verified)"
    }


@app.get(
    "/secure",
    dependencies=[Depends(auth.implicit_scheme)],
    responses=security_responses,
)
async def get_secure(user: Auth0User = Security(auth.get_user)):
    return user


@app.get("/also-secure")
async def get_also_secure(user: Auth0User = Security(auth.get_user)):
    return user


@app.get("/also-secure-2", dependencies=[Depends(auth.get_user)])
async def get_also_secure_2():
    return {"message": "I dont care who you are but I know you are authorized"}


@app.get("/secure-scoped")
async def get_secure_scoped(
    user: Auth0User = Security(auth.get_user, scopes=["read:scope1"])
):
    return user


@app.get("/secure-custom-user")
async def get_secure_custom_user(
    user: CustomAuth0User = Security(auth_custom.get_user),
):
    return user
