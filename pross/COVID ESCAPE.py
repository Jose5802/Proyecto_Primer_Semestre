import arcade
import random
import time
import os


SCREE_WIDHT = 1200
SCREE_HEIGHT = 600
SCREE_TITLE = "COVID ESCAPE"


# constantes para escalar sprites
escala_personaje = 0.9
escala_virus = 0.15
escala_piso = 0.5
escala_pisovolador = 0.5
escala_guantes = 0.05
escala_mask = 0.10
escala_gel = 0.07
escala_sol = 0.5

# características de la fisica del juego
JUMP_SPEED = 15
GRAVITY = 3
MOVEMENT_SPEED = 5

# Cuántos píxeles para mantener como margen mínimo entre el personaje
# y el borde de la pantalla.
#LEFT_VIEWPORT_MARGIN = 0
#RIGHT_VIEWPORT_MARGIN = 0
#BOTTOM_VIEWPORT_MARGIN = 0
#TOP_VIEWPORT_MARGIN = 0

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREE_WIDHT, SCREE_HEIGHT, SCREE_TITLE)
        arcade.set_background_color(arcade.color.ALICE_BLUE)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.player_list = None  # LISTA QUE CONTIENE PERSONAJE
        self.virus_list = None  # ...
        self.pisos_list = None
        self.objetos_list = None
        self.decoración_list = None

        self.player_sprite = None  # VARIABLE DEL SPRITE
        self.virus_sprite = None  # VARIABLE DEL SPRITE
        self.pisos_sprite = None  # ...
        self.objetos_sprite = None
        self.decoración_sprite = None

        self.physics_engine = None  # le damos características de la función physics_engine a nuestro objeto
        self.wall_list = None  # creamos esta característica para más adelante poder identificar ciertos objetos que no se pueden atravesar (piso, piso flotante).

        self.collect_objetos_sound = arcade.load_sound("Recoger.mp3") #Sonido cuando toma cosas el personaje
        self.jump_sound = arcade.load_sound("salto.mp3") #Efecto de sonido cuando salta el personaje

        # Se utiliza para realizar un seguimiento de nuestro desplazamiento
        self.view_bottom = 0
        self.view_left = 0

        self.score = 0 #Lleva un registro de la puntuación

    def setup(self):  # inicializar las listas
        self.player_list = arcade.SpriteList()  # VA PERMITIR CONTROLAR COLISIONES/MOVIMIENTO
        self.virus_list = arcade.SpriteList()
        self.pisos_list = arcade.SpriteList()
        self.objetos_list = arcade.SpriteList()
        self.decoración_list = arcade.SpriteList()

#        self.player_list.append(self.player_sprite)
        self.wall_list = arcade.SpriteList()
        #AMBIENTE
        sol = "sun1.png"
        self.decoración_sprite = arcade.Sprite(sol, escala_sol)
        self.decoración_sprite.center_x = 74
        self.decoración_sprite.center_y = 560
        self.decoración_list.append(self.decoración_sprite)

        letrero = "sign.png"
        self.decoración_sprite = arcade.Sprite(letrero, 0.7)
        self.decoración_sprite.center_x = 670
        self.decoración_sprite.center_y = 108
        self.decoración_list.append(self.decoración_sprite)

        piedra_x = [200,690]
        for k in range(len(piedra_x)):
            piedra = "rock.png"
            self.decoración_sprite = arcade.Sprite(piedra, 0.3)
            self.decoración_sprite.center_x = piedra_x[k]
            self.decoración_sprite.center_y = 80
            self.decoración_list.append(self.decoración_sprite)

        # Se utiliza para realizar un seguimiento de nuestro desplazamiento
        self.view_bottom = 0
        self.view_left = 0
        #Puntuación
        self.score = 0 #Lleva un registro de la puntuación


        for i in range (0,1200,150):
            pasto = arcade.Sprite("grass.png", escala_sol)
            pasto.center_x = i
            pasto.center_y = 93
            self.decoración_list.append(pasto)


        # Crear personaje
        personaje = "adventurer_swim1.png"
        self.player_sprite = arcade.Sprite(personaje, escala_personaje)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 93
        self.player_list.append(self.player_sprite)

        # CREAR VIRUS
        virus = "virus.png"
        self.virus_sprite = arcade.Sprite(virus, escala_virus)
        self.virus_sprite.center_x = 1107
        self.virus_sprite.center_y = 105
        self.virus_list.append(self.virus_sprite)

        # crear piso con un loop de la imagen
        for i in range(0, 1300, 64):
            piso = arcade.Sprite("grassMid.png", escala_piso)
            piso.center_x = i
            piso.center_y = 32
            self.pisos_list.append(piso)
            self.wall_list.append(piso)  # el piso no se puede atravesar

        # asignar coordenadas fijas a el piso flotante
        coordenas_pisoflotante = [[64,320],[600,200],[520, 430],[650,430], [930,430],[255, 200], [945, 200], [400, 320], [780, 320],[1107, 310], [180, 460], [1107, 450]]
        n = 1
        cosas = ["alcohol gel.png", "guantes.png", "mascara.png"]
        cte_eje_y = 50
        while n <= 9:
            coordenas__choicepisoflotante = random.choice(coordenas_pisoflotante)
            coordenas_pisoflotante.remove(coordenas__choicepisoflotante)

            cordenadas_lista=[coordenas__choicepisoflotante]

            for p in cordenadas_lista:
                pisoaire=arcade.Sprite("ground_grass_small_broken.png",escala_pisovolador)
                pisoaire.position=p
                self.pisos_list.append(pisoaire)
                self.wall_list.append(pisoaire)  # el piso flotante no se puede atravesar
                n=n+1


                o = random.choice(cosas)

                if o == "alcohol gel.png":
                    material = arcade.Sprite(o, escala_gel)
                    material.position = p[0],p[1]+cte_eje_y
                    self.objetos_list.append(material)

                elif o == "guantes.png":
                    material = arcade.Sprite(o, escala_guantes)
                    material.position = p[0],p[1]+cte_eje_y
                    self.objetos_list.append(material)

                elif o == "mascara.png":
                    material = arcade.Sprite(o, escala_mask)
                    material.position = p[0],p[1]+cte_eje_y
                    self.objetos_list.append(material)




       # coordenas_pisoflotante = [[600, 430], [255, 200], [945, 200], [420, 320], [780, 320], [180, 460], [1107, 450]]
        #for p in coordenas_pisoflotante:
         #   pisoaire = arcade.Sprite("Piso flotante.png", escala_pisovolador)
          #  pisoaire.position = p
           # self.pisos_list.append(pisoaire)
            #self.wall_list.append(pisoaire)  # el piso flotante no se puede atravesar



        # le agregamos gravedad a nuestro personaje sin permitirle atravesar el piso ni el piso flotante.
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list)

    def gravedad(self):
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

    def on_draw(self):
        arcade.start_render()
        self.decoración_list.draw()
        arcade.draw_text("PELIGRO!\nCOVID-19",670,111,arcade.color.DARK_CANDY_APPLE_RED,15, width=100, align="center",
                         anchor_x="center", anchor_y="center")
        self.player_list.draw()
        self.virus_list.draw()
        self.pisos_list.draw()
        self.objetos_list.draw()
        self.wall_list.draw()

        #Dibuja nuestro puntaje en la pantalla, desplazándolo con la ventana gráfica
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 , 10 , arcade.csscolor.WHITE, 18)


    def on_key_press(self, key, modifiers):  # se llama cada vez que presionamos una tecla

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
                arcade.play_sound(self.jump_sound)#Efecto sonido de salto cuando se presiona la tecla "UP"
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):  # para cuando el usuario suelta la tecla
        """Called when the user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):  # Actualización
        self.physics_engine.update()

        #Mira si golpeamos algun objeto
        objetos_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.objetos_list)
        #Recorre cada objeto que golpeamos (si hay alguno) y lo retira el objeto de  para monedas en objetos_hit_list:
        for objetos in objetos_hit_list:
            # Remueve el objeto
            objetos.remove_from_sprite_lists()
            # Hace un sonido al "tomar" el objeto
            arcade.play_sound(self.collect_objetos_sound)
            self.score += 1 #Agrega uno al puntaje

        # --- Administrar desplazamiento ---

        # Rastrear si necesitamos cambiar la ventana gráfica
        #changed = False

        # Desplazarse a la izquierda
        #left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        #if self.player_sprite.left < left_boundary:
            #self.view_left -= left_boundary - self.player_sprite.left
            #changed = True

        # Desplazarse a la derecha
        #right_boundary = self.view_left + SCREE_WIDHT - RIGHT_VIEWPORT_MARGIN
        #if self.player_sprite.right > right_boundary:
            #self.view_left += self.player_sprite.right - right_boundary
            #changed = True

        # Desplazarse hacia arriba
        #top_boundary = self.view_bottom + SCREE_HEIGHT - TOP_VIEWPORT_MARGIN
        #if self.player_sprite.top > top_boundary:
            #self.view_bottom += self.player_sprite.top - top_boundary
            #changed = True

        # Desplazarse hacia abajo
        #bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        #if self.player_sprite.bottom < bottom_boundary:
            #self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            #changed = True

        #if changed:
            # Solo desplazamiento en enteros. De lo contrario, terminamos con píxeles que
            # no se alineen en la pantalla
            #self.view_bottom = int(self.view_bottom)
            #self.view_left = int(self.view_left)

           # Do the scrolling
            #arcade.set_viewport(self.view_left,
                                #SCREE_WIDHT + self.view_left,
                                #self.view_bottom,
                                #SCREE_HEIGHT + self.view_bottom)
def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
