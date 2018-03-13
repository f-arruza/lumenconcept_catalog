### Microservicios incluidos:
##### 1.) Catalog Manager (API REST)
##### 2.) Offer Manager (API REST)
##### 3.) Offer Verification (Backgroung Task)

###### TODOS desplegables de manera independiente en contenedores Docker.
###### Para iniciar los procesos en segundo plano, se debe ejecutar el siguiente comando: 
python manage.py process_tasks

###### La implementación del punto tres (3) la puede encontrar en: 
lumenconcept_catalog/catalog/tasks.py 
