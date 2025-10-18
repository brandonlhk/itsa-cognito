You can build the Dockerfile and look at the documentation via `localhost:8000/docs`

You would need the `.env` file as well

`DATABASE_URL=mysql+pymysql://root@host.docker.internal:3306/itsa`
`JWT_SECRET=<anything>`
`JWT_ALGORITHM=HS256`
`JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60`

Then run the docker build command:
`docker build -t crm-user-service .`

Then run the container and inject .env file
`docker run --rm -p 8000:8000 --env-file .env crm-user-service`

## Currently these are the routes:
1. Authenticate [Returns JWT] || This will return a JWT which you have to attach to every protected route in the form of `Bearer <JWT>`
2. Admin | Create new user || Admin protected route, creates a new user
3. Admin | Update user || Admin protected route, currently updates user's name
4. Admin | Disable user || Admin protected route, disables a user
5. Admin | Delete user || Admin protected route, deletes a user (Agent/Admin). Root admin (id: 1) is protected from this action
6. Reset Password - Initiate || This sends a token to the user, currently its sent back to the browser
7. Reset Password - Perform || Attaching the token, the user is able to reset their password