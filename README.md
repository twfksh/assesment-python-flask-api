# 🚀 Flask Auth API Backend

A modular Flask backend service featuring user authentication, database utilities, and service-based architecture. Managed using the ultra-fast `uv` package manager.


## 📦 Features

- 🔐 User authentication (register/login/logout), JWT(refresh), protected routes(whoami,users/all)
- ⚙️ Database utility functions
- 👤 User & Auth service logics
- 📁 Modular and scalable project structure following dependency injection principles
- ⚡ Fast dependency management with `uv` package manager


## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-project.git
cd your-project
```

### 2. Create `.env` file

Copy the sample environment file and fill in required values:

```bash
cp .env.sample .env
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Run the application

```bash
uv run python -m flask run
```