# 🤖 Sistema de Control de Brazo Robótico - Robótica 8vo Semestre

Un sistema completo para el control y visualización en tiempo real de un brazo robótico de 3 grados de libertad con interfaz web 3D interactiva.

## 🎯 Características Principales

- **Visualización 3D en Tiempo Real**: Representación visual del brazo robótico con animaciones suaves
- **Control Dual**: Modos secuencial y paralelo para programación de movimientos
- **Autenticación Segura**: Sistema de login con JWT para administradores
- **Persistencia en Firebase**: Almacenamiento del estado y programas en la nube
- **Comunicación WebSocket**: Sincronización en tiempo real entre cliente y servidor
- **Interfaz Moderna**: UI responsive con diseño glassmorphism

## 🏗️ Arquitectura del Sistema

### Frontend (Cliente)
```
client/
├── src/
│   ├── components/         # Componentes React
│   │   ├── Robot3D.tsx    # Visualización 3D del robot
│   │   ├── Controls.tsx   # Controles de movimiento
│   │   ├── Login.tsx      # Autenticación
│   │   └── ...
│   ├── context/           # Contextos React
│   │   ├── AuthContext.tsx
│   │   └── SocketContext.tsx
│   ├── services/          # Servicios API
│   └── hooks/             # Custom hooks
└── package.json
```

### Backend (Servidor)
```
backend/
├── app/
│   ├── main.py           # Punto de entrada FastAPI
│   ├── auth.py           # Autenticación JWT
│   ├── robot.py          # Lógica del robot y colas
│   ├── core/
│   │   ├── config.py     # Configuración
│   │   └── firebase.py   # Integración Firebase
│   ├── api/routes/       # Rutas HTTP
│   └── websocket/        # Endpoints WebSocket
├── requirements.txt
└── .env
```

## 🚀 Tecnologías Utilizadas

### Frontend
| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| **React** | 19.1.1 | Framework principal para la interfaz de usuario |
| **TypeScript** | 5.8.3 | Tipado estático para JavaScript |
| **Vite** | 7.1.2 | Build tool y servidor de desarrollo |
| **Three.js** | 0.170.0 | Motor gráfico 3D para WebGL |
| **@react-three/fiber** | 9.0.0 | Renderer React para Three.js |
| **@react-three/drei** | 10.7.2 | Helpers y utilidades para R3F |
| **Tailwind CSS** | 4.1.12 | Framework CSS utility-first |
| **Axios** | 1.7.7 | Cliente HTTP para APIs |
| **ESLint** | 9.33.0 | Linter para código JavaScript/TypeScript |

### Backend
| Tecnología | Descripción |
|------------|-------------|
| **FastAPI** | Framework web moderno y rápido para APIs |
| **Python** | 3.13+ Lenguaje de programación principal |
| **Uvicorn** | Servidor ASGI para aplicaciones Python |
| **Pydantic** | Validación de datos y serialización |
| **WebSockets** | Comunicación bidireccional en tiempo real |
| **SQLModel** | ORM basado en SQLAlchemy y Pydantic |
| **Firebase Admin SDK** | Integración con servicios Firebase |
| **Python-JOSE** | Manejo de tokens JWT |
| **Passlib** | Hashing seguro de contraseñas |
| **Python-dotenv** | Gestión de variables de entorno |

### Base de Datos y Servicios
| Servicio | Propósito |
|----------|-----------|
| **Firebase Firestore** | Base de datos NoSQL para programas guardados |
| **Firebase Realtime DB** | Sincronización en tiempo real del estado del robot |
| **Firebase Storage** | Almacenamiento de archivos (futuras expansiones) |

### Herramientas de Desarrollo
| Herramienta | Propósito |
|-------------|-----------|
| **VS Code** | Editor de código principal |
| **Git** | Control de versiones |
| **ESLint + TypeScript ESLint** | Análisis estático de código |
| **PostCSS** | Procesamiento de CSS |
| **Autoprefixer** | Compatibilidad CSS cross-browser |

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Node.js 18+ 
- Python 3.13+
- Cuenta de Firebase (opcional, para persistencia)

### Backend
```bash
cd backend

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# o
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de Firebase

# Ejecutar servidor
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd client

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev

# Build para producción
npm run build
```

## 🔧 Configuración de Firebase

1. Crear proyecto en [Firebase Console](https://console.firebase.google.com)
2. Habilitar Firestore Database y Realtime Database
3. Descargar archivo de credenciales del Service Account
4. Configurar variables de entorno:

```env
FIREBASE_CREDENTIALS_PATH=./ruta/al/archivo-credenciales.json
FIREBASE_PROJECT_ID=tu-project-id
FIREBASE_DATABASE_URL=https://tu-proyecto.firebaseio.com
FIREBASE_STORAGE_BUCKET=tu-proyecto.appspot.com
```

## 🎮 Uso del Sistema

### Modos de Control

#### Modo Secuencial
- Los movimientos se ejecutan uno tras otro
- Ideal para movimientos precisos y coordinados
- Cada comando especifica: articulación, ángulo y duración

#### Modo Paralelo  
- Todas las articulaciones se mueven simultáneamente
- Perfecto para posicionamiento rápido
- Cada comando especifica: base, hombro, codo y duración

### Articulaciones del Robot
- **Base**: Rotación en el eje Y (0° - 180°)
- **Hombro**: Elevación del brazo superior (0° - 180°)
- **Codo**: Flexión del antebrazo (0° - 180°)

## 📊 API Endpoints

### Autenticación
```http
POST /auth/login     # Iniciar sesión
POST /auth/logout    # Cerrar sesión
GET  /auth/me        # Información del usuario
```

### Control del Robot
```http
GET  /robot/state           # Obtener estado actual
POST /robot/state           # Establecer nueva posición
POST /robot/sequential/enqueue  # Encolar movimiento secuencial
POST /robot/parallel/enqueue    # Encolar movimiento paralelo
POST /robot/sequential/start    # Ejecutar cola secuencial
POST /robot/parallel/start      # Ejecutar cola paralela
```

### WebSocket
```
ws://localhost:8000/ws      # Conexión WebSocket para eventos en tiempo real
```

## 🎨 Interfaz de Usuario

### Características de la UI
- **Diseño Responsive**: Adaptable a diferentes tamaños de pantalla
- **Tema Oscuro**: Esquema de colores moderno con efectos glassmorphism
- **Visualización 3D Interactiva**: 
  - Rotación: Click izquierdo + arrastrar
  - Zoom: Scroll del mouse
  - Paneo: Click derecho + arrastrar
- **Feedback Visual**: Animaciones suaves y indicadores de estado
- **Controles Intuitivos**: Sliders para control de ángulos

## 🔒 Seguridad

- **Autenticación JWT**: Tokens seguros con expiración
- **Autorización por Roles**: Solo administradores pueden controlar el robot
- **Validación de Datos**: Pydantic para validación en backend
- **CORS Configurado**: Política de orígenes cruzados controlada
- **Variables de Entorno**: Credenciales protegidas

## 🚀 Despliegue

### Producción
```bash
# Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
npm run build
# Servir archivos estáticos con nginx/apache
```

### Docker (Futuro)
```dockerfile
# Configuración Docker pendiente de implementar
```

## 🧪 Testing

```bash
# Backend
pytest

# Frontend  
npm run test
```

## 📈 Roadmap Futuro

- [ ] Integración con hardware real del brazo robótico
- [ ] Grabación y reproducción de secuencias
- [ ] Simulación de física realista
- [ ] Control por voz
- [ ] Aplicación móvil complementaria
- [ ] Dashboard de métricas y analytics
- [ ] Contenedorización con Docker
- [ ] CI/CD pipeline
- [ ] Testing automatizado

## 👥 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto es parte del curso de Robótica - 8vo Semestre.

## 🎓 Créditos

**Desarrollado con 💫 por el equipo de Robótica - 8vo Semestre**

---

## 📞 Soporte

Para preguntas o problemas:
- 📧 Email: [achavezc1@est.emi.edu.bo]
- 🐛 Issues: [GitHub Issues](https://github.com/Danilo0125/robotica/issues)
- 📚 Documentación: [Wiki del Proyecto](https://github.com/Danilo0125/robotica/wiki)

---

*Última actualización: Agosto 2025*
