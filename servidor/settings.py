from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DATE_INPUT_FORMATS = ['%d-%m-%Y']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r$mzm&y@2au1v-ys4ab9qz2#y-p@e*9^h8x_pva$g^013wlb5v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]
"""
#SECURE_SSL_REDIRECT =True #todas de http a https
#SECURE_BROWSER_XSS_FILTER = True # prevenir inyeccion de scripts en las url
    #validar y limpiar bien los datos ingresados
    #django trae esta seguridad incorporada al activarla


#CORS 
    #mec. de seguridad, para solicitar RESTs data desde otro dominio que no sea el mismo del servidor 
    #por defecto se bloquea peticiones como las APIS exteriores
    #Validar CORS para las APIS del Condominio y Oficiales
    #Incorporar aplicacion de ZONA SUR APIs

#configurarion
    #pip install django-core-headers
    
MIS_CORS=[
    #"corsheaders",
]

MIS_MIDDLEWARE = [
    #"corsheaders.middleware.CorsMiddleware",
]

    #MIDDLEWARE : CorsMiddleware
        #funciones que se ejecutan antes de llegar al view final, peticiones http, 
        #gestina y manipula las solicitudes y respuestas http



CORS_ALLOW_ALL_ORIGIN = True #Desde todos los servidores # no recomendado para produccion 

#permitir solo ips confiables, 

CORS_ALLOW_CREDENTIALS= True #permite el uso de credenciales como cookies y encabezados
    #intercamvbio de datos sencibles entre , APIS


#Dominios permitidos
CORS_ORIGIN_WHITELIST=[
   # "https://dominios-permitido.com",
]
    
     
#Proteger informacion, peticiones de autenticacion seguros
    
SESSION_COOKIES_SECURE = True #Solo se envian por https
#similar pero se aplica al csrf
CSRF_COOKIES_SECURE = True #de cookies CSRF

SESSION_COOKIES_HTTPONLY = True #previene ataques de sesion javascript, protegiendolas de ataques XSS
#asegura csrf tambien
CSRF_COOKIES_HTTPONLY = True 

SESSION_COOKIES_SAMESITE = "Lax" #previene que las cookies sean enviadas en solicitud cross site
#asegurate en el view.py


_summary_
    
    def agregar_Sec_cookies(request):
        
        var_response = HttpResponse ("Cookie configurada)
        
        var_response.set_cookie( 
            'nombre_cooki',
                'valor_cooki',
                    max_age=3600 #duracion en segundos antes que expire,
                    secure=True #Solo se envie atraver de https,
                    httponly=True #previene que la cookie sea accedida desde javascrip, protegiendola de ataques xss,
                    samesite='Lax' #Define como se comporta la cookie en solicitud cross-site , ayudando a prevenir ataques csrf
        )
        return var_response
    
    def obtener_Sec_cookies(request):
        valores_cookies = request.COOKIES.get ("nombre_cooki")
        return HttpResponde ( f"Valor de la cookie: { valor_cooki } " )


    Ataque CSRF: 
        atacante induce a un usuario logeado a realizar acciones no deseadas al servidor
            ejemplo:
                el atacante te envia un link, tu le das clck y entras a tu navegador donde estas logeado con tu cuenta bancaria ,
                    en las cookies que te hace enviar va estos datos , valida tu usuario y hace una transferencia de 10k y listo    
        Protección:
            CSRF TOKENS: un token unico es generado y enviado en cada solicitud
            SAMESITE: configura las cookies con el atributo samesite 
                previene datos sean enviado cross-site 
                            #ocurre cuando una pagina web solicita un http a un dominio diferente CROSS-SITE
    Ataque JAVASCRIPT XSS cross site scripting
        el atacante inyecta scripts maliciosos, estos scrps realizan funciones dentro del navegador del usuario y extrae sus cookies redirigir a otros lugares etc
            ejemplo:
                en un campo del formulario el atacante inyecta un scripts, y se ejecuta por el usuario robando cookies etc
        Proteccion:
            asegurar que cualquier dato del usuario sea analizado antes de ser enviado y mostrado
            valida los datos de entrada por el usuario 
            content security policy CSP : defina politicas de seguridad que restringa
    """
    
    

DJANGO_APPS=[ 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize'
]

MIS_APPS = [
    'portafolio','accounts', 'condominio',  'oficiales', 'gyna', 'tiendas', 'widget_tweaks', 'blog', 'factus', 'repuestos', 
    ]

INSTALLED_APPS = DJANGO_APPS + MIS_APPS 
#+ MIS_CORS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'servidor.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'servidor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Configura tu base de datos usando la URL proporcionada por el entorno
#DATABASES = { 'default': dj_database_url.config( default=os.environ.get('DATABASE_URL') ) } 

#POSTGRES_URI = os.getenv( "POSTGRES_URI", "postgresql://ecomycr:w9M5on5qUPZebxrac9JXMbnfVhE6TCSx@dpg-ctiv2abtq21c73dv4h00-a/ecomycr_ift4" )


#clean code: seguridad en datos de .env


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


#sqlite3
"""



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  "ecomycr",  #os.getenv('DB_NAME'),
        'USER': "ecomycr", #os.getenv('DB_USER'),
        'PASSWORD': "zbyj8918", #os.getenv('DB_PASSWORD'),
        'HOST': "localhost", #os.getenv('DB_HOST', 'localhost'),
        'PORT': "3306", #os.getenv('DB_PORT', '3306'),
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yera8922$ecomycr',
        'USER': 'yera8922',
        'PASSWORD': 'zbyj8918',
        'HOST': 'yera8922.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}

#sqlite3

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

import os
from dotenv import load_dotenv


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}
"""

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Costa_Rica'

USE_I18N = True # para internacionalizacion, preparar una aplicacion para que pueda ser adaptada a diferentes idiomas
USE_TZ = False #Uso de zonas horarias



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


SECOND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(SECOND_DIR,'static' ),
    os.path.join(SECOND_DIR, 'portafolio','static' ),    
    os.path.join(SECOND_DIR, 'repuestos','static' ),     
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')




#sistema de login django
LOGIN_REDIRECT_URL ='/'
LOGOUT_REDIRECT_URL ='proyectos'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#SMTP SETTINGS PARA ENVIAR EMAILS DE RESTABLECIMIENTO DE PASSWORD
#Estos datos van dentro del dotenv .env

#EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend" #configuracion del backend django servidor
EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend" #para pruebas emails
EMAIL_HOST = "smtp.gmail.com" #dejo en los pdf alguna de estas configuraciones para email o outlook etc
EMAIL_PORT = 587



EMAIL_SSL=True
EMAIL_USE_TLC =False #Transport layer security : para la conexion smtp 

#ESTOS DATOS AGREGALOS EN EL ARCHIVO .ENV
EMAIL_HOST_USER= "ecotraXXXXXbajo8@gmail.com"
EMAIL_HOST_PASSWORD = "XXXXXXXXX"





#manejas donde guardamos la foto que sube el usuario 
# Ruta al directorio de medios
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


