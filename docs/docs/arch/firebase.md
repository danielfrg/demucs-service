# Firebase

<figure markdown>
![firebase](https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Firebase_Logo.svg/1280px-Firebase_Logo.svg.png){: style="height:100px"}
</figure>

[Firebase](https://firebase.google.com/) provides easy hosting of web applications
plus a lot of other features like user Authentication, managed database infrastructure,
and really clean client APIs to interact with the services.

The Firebase project has one web application because we only have a web
frontend but other clients can easily be added and the firebase infrastructure
would stay the same.

<figure markdown>
![firebase](/docs/public/images/firebase-project.png){: style="height:100px"}
</figure>

## Authentication

Firebase allows us to easily activate multiple authentication methods
on our case we only activate Google.

<figure markdown>
![firebase](/docs/public/images/firebase-signin.png)
<figcaption>Firebase Auth</figcaption>
</figure>

<figure markdown>
![firebase](/docs/public/images/firebase-users.png)
<figcaption>Firebase users</figcaption>
</figure>

## WebApp

See [Web App](/docs/arch/webapp) to see how it interacts with Firebase.
