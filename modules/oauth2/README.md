# OAUTH 2.0 MODULE

## Overview

The OAuth 2.0 module is designed to facilitate the implementation of the OAuth 2.0 authorization framework. It provides a set of classes and functions that allow developers to easily integrate OAuth 2.0 authentication into their applications.
This module is particularly useful for applications that need to authenticate users via third-party services such as Google, Facebook, or GitHub and normal username/password authentication.

## Features

- **Authorization Code Flow**: Supports the standard OAuth 2.0 authorization code flow, including token exchange and refresh token handling.

1. `TokenPayloadBase` class

The `TokenPayloadBase` class is used to define the payload structure for the token. This class is a base class that can be extended to create custom payload classes for different requirements. It includes common fields such as `sub`, `exp` which are standard claims in JWT tokens. And also includes the `role` field which can be used to define the role of the user in the application.

Receives a Generic type argument for `UserRoleType` parmam which is used to define the type of the `role` field. This allows you to use any type for the `role` field, such as a string, integer, or enum. By default `UserRoleType` is `str`.

Some other common fields will be added: `iat` (The token issued time. Example: `iat: 1516239022`); `scope`: (The scope of the token. Examples: `scope: "https://www.googleapis.com/auth/userinfo.profile"`); `provider` (The token provider. Example: `provider: "google"`).

The `TokenPayloadBase` needs to be extended by a class that brings additional fields to satisfy the requirements of the application. For example, if you want to include the user's email address in the token payload, you can create a class that extends `TokenPayloadBase` and adds an `email` field.

2. `AccessToken` class

The `AccessToken` class is used to represent the access token that is returned by the OAuth provider after the user has authenticated. This class includes fields such as `access_token` and `token_type`. The `access_token` field is the actual token that is used to authenticate the user with the OAuth provider. The `token_type` field indicates the type of token that is being returned, such as "Bearer".
This class receives as Generic type argument for `CustomizedGenericTokenPayload` param which represents the tructure of the token payload. NOTE that the given class must extend `TokenPayloadBase` class.

This class has the `.verify(token, TokenPayloadClass, token_required)` class method that is used to verify the access token. This method takes the token as a string and the class that represents the token payload as arguments. It also takes an optional `token_required` argument which indicates whether the token is required or not. If the token is not required and is not provided, the method will return None. If the token is required and is not provided, the method will raise an exception.
The method will decode the token and verify its signature using the public key of the OAuth provider. If the token is valid, it will return an instance of the `TokenPayloadClass` with the decoded payload. If the token is invalid, it will raise an exception. NOTE that the `TokenPayloadClass` must extend the `TokenPayloadBase` class.
