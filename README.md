# Riviera_ThePromisedLand
Tools to translate text in the .gba game Riviera: The Promised Land  

Translating:  
The `Scripts` folder includes all game scripts with the configuration of the Atlas program.  
You have to add the translated text of each string, keeping the `<..>` control codes.  

![Text](https://github.com/user-attachments/assets/c406fcfd-f144-4a9f-8c03-1ec11cc1ed92)


Editing the font:  
Applying the `RTPL.ups` patch to the `TLP.gba` rom activates the option to edit the font.  

![Edit](https://github.com/user-attachments/assets/58c71ab5-bccf-4912-811c-ee4556359f8b)

Graphically you can use the tiles between 0x58B400 0x58C403, from  
AA to FB and edit their widths in the table at the offset  
0x1031450 to 0x1031503, this table includes all the tile widths you see in the image above.  

Inserting the text:  
You need to modify the IN.tbl table to include the characters of your language.  
using the Hex=Glyph conversion, preferably from (AA to FB).  
Paste into the `Insert` folder the translated scripts and run the file `Atlas_Insert.bat`.  

If everything went well, the resulting file will be `TPL_translation.gba`.



# Riviera_ThePromisedLand
Herramientas para traducir el texto del juego Riviera: The Promised Land  

Traduciendo:  
La carpeta `Scripts` incluye todos los scripts del juego con la configuracion  
del programa Atlas.  
Hay que agregar el texto traducido en cada string, conservando los codigos de control `<..>`  

![Text](https://github.com/user-attachments/assets/c406fcfd-f144-4a9f-8c03-1ec11cc1ed92)


Editando la fuente:  
Al aplicar el patch `RTPL.ups` al rom `TLP.gba` se activan la opcion para editar la fuente.  

![Edit](https://github.com/user-attachments/assets/58c71ab5-bccf-4912-811c-ee4556359f8b)

Graficamente puedes usar los tiles entre 0x58B400 0x58C403, es decir desde  
AA hasta FB y editar sus anchos en la tabla que se encuentra en el offset  
0x1031450 hasta 0x1031503, esta tabla incluye todos los anchos de los tiles  
que se ven en la imagen.  

Insertar el texto:  
Modificas la tabla IN.tbl para que incluya los caracteres de tu idioma.  
usando la conversion Hex=Glyph. preferiblemente desde (AA hasta FB)  
Pegas dentro de la carpeta `Insert` los scripts traducidos y ejecutas el  
archivo `Atlas_Insert.bat`  

Si todo ha ido bien, el archivo resultante será `TPL_translation.gba`
