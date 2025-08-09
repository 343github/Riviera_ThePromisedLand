# Riviera_ThePromisedLand
Tools for translating Riviera: The Promised Land game text

Translating:  
The `Scripts` folder includes all the game scripts with the Atlas program configuration.  
Add the translated text to each string, keeping the `<..>` control codes.

![Text](https://github.com/user-attachments/assets/c406fcfd-f144-4a9f-8c03-1ec11cc1ed92)

Editing the font:  
Run the `Font_Extractor.py` script; this will extract the game font.

<img width="160" height="120" alt="Font" src="https://github.com/user-attachments/assets/8669966f-d6ff-44d5-93ad-0da23f5586e4" />

You can modify this font to your liking using an editing program like Aesprite or Photoshop.
It must be a color-indexed program so that there are no errors when inserting it again.

<img width="371" height="144" alt="image" src="https://github.com/user-attachments/assets/d78714d0-aac6-492a-aa3d-8e0338a7cd5e" />

After finishing your font editing, open the `widths.txt` file and enter the width value for each modified character.
This game only accepts values from 0.1 pixel to 10 pixels.

<img width="409" height="229" alt="image" src="https://github.com/user-attachments/assets/7e5a836e-ddb2-4917-a07a-39e04b4a0d52" />

With the font and its widths defined, all that's left to do is run the `Font_Inserter.py` script.
This file will modify the ROM with the new font and its widths.

Insert the text:  

Modify the `IN.tbl` table in the `/insert` folder to include the characters for your language.
Using the Hex=Glyph conversion. From (AA to FB)

<img width="200" height="403" alt="image" src="https://github.com/user-attachments/assets/748d855b-fcaf-45e3-b3cd-84d854929665" />

You paste the translated scripts `(tpl_script_000.txt,tpl_script_001.txt...tpl_script_039.txt)` into the `Insert` folder and execute the
file `Atlas_Insert.bat`

If everything went well, the resulting file will be `TPL_translation.gba`





# Riviera_ThePromisedLand
Herramientas para traducir el texto del juego Riviera: The Promised Land  

Traduciendo:  
La carpeta `Scripts` incluye todos los scripts del juego con la configuracion  
del programa Atlas.  
Hay que agregar el texto traducido en cada string, conservando los codigos de control `<..>`  

![Text](https://github.com/user-attachments/assets/c406fcfd-f144-4a9f-8c03-1ec11cc1ed92)


Editando la fuente:  
Ejecuta el script `Font_Extractor.py` esto extraerá la fuente del juego.

<img width="160" height="120" alt="Font" src="https://github.com/user-attachments/assets/8669966f-d6ff-44d5-93ad-0da23f5586e4" />

Puedes modificar esta fuente a tu gusto usando un programa de edicion como Aesprite o photoshop.
debe ser un programa con color indexado para que no haya errores al insertar de nuevo.

<img width="371" height="144" alt="image" src="https://github.com/user-attachments/assets/d78714d0-aac6-492a-aa3d-8e0338a7cd5e" />

luego de terminar tu edicion de la fuente, abre el archivo `widths.txt` e inserta el valor del ancho de cada caracter modificado,  
este juego solo acepta valores desde 01 pixel hasta 10 pixeles.  

<img width="409" height="229" alt="image" src="https://github.com/user-attachments/assets/7e5a836e-ddb2-4917-a07a-39e04b4a0d52" />

Con la fuente y sus anchos definidos, solo falta ejecutar el script `Font_Inserter.py`
este archivo modificará el rom con la nueva fuente y sus anchos.

Insertar el texto:  
Modificas la tabla `IN.tbl` dentro de la carpeta `/insert` para que incluya los caracteres de tu idioma.  
usando la conversion Hex=Glyph. 
Desde (AA hasta FB)  

<img width="200" height="403" alt="image" src="https://github.com/user-attachments/assets/748d855b-fcaf-45e3-b3cd-84d854929665" />

Pegas dentro de la carpeta `Insert` los scripts traducidos `(tpl_script_000.txt,tpl_script_001.txt...tpl_script_039.txt)` y ejecutas el  
archivo `Atlas_Insert.bat`  

Si todo ha ido bien, el archivo resultante será `TPL_translation.gba`
