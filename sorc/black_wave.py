
class BlackWave(Spell):
    def cast(self, context):
        counter = 0
        counter_max = 8

        # if context.is_active():
        #     print(f"Casting: {self.name}")
        #         self.bind.press()
        #         while(self.ready(debug=debug) and counter < counter_max and context.is_active()):
        #             counter += 1
        #             time.sleep(0.08)
            
        #     if counter >= 8:
        #         print("Spell cast failed")
        #         self.bind.release()
        #         return False
        #     elif not context.is_active():
        #         self.bind.release()
        #         if self.ready(debug=debug):
        #             print("Spell cast not completed")
        #             return False
        #         else:
        #             self.shared_data.last_cast = time.time()
        #             return True
        #     else:
        #         self.shared_data.last_cast = time.time()
        #         self.bind.hold_and_release(context, self.duration, self.speed_function())
        #         return True