# confirm-user-app

Pyforms Web application that allows the superuser to confirm the access to registered users.


## Usage

> **Not available on PyPI**

Clone the repo and add the application to `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    # ...
    "confirm_users.apps.ConfirmUsersConfig",
    # ...
]
```

## Configuration

Available settings:

- `USER_EDIT_FORM` (`"confirm_users.apps.user.UserForm"`)

	Specifies the Pyforms `ModelFormWidget` to edit user data, if needed.
