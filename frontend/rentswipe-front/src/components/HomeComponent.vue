<script>
export default {
    data(){
        return{

        }
    },
    methods:{
    }
} 

</script>
<template>
    <div id = "home">
        <v-row no-gutters>
            <v-col cols="3">
                <v-sheet class="pa-2 ma-2">
                    
                <img src="https://i.imgur.com/805Iiug.png" alt = "logo" style="width: 100px; height: 20px;"/>
                </v-sheet>
            </v-col>
            <v-col cols="2">
                <v-sheet class="pa-2 ma-2">
                    <p>How it works</p>
                </v-sheet>
            </v-col>
            <v-col cols="2">
                <v-sheet class="pa-2 ma-2">
                    <p>Pricing</p>
                </v-sheet>
            </v-col>
            <v-col cols="2">
                <v-sheet class="pa-2 ma-2">
                    <p>Testimonials</p>
                </v-sheet>
            </v-col>
        </v-row>
        <v-row no-gutters>
            <v-col cols="5">
                <v-sheet class="pa-2 ma-2">
                    <h1 style="font-size: 2.5em;">The only tool you</h1>
                    <h1 style="font-size: 2.5em;">need to find a home</h1>
                    <p>Find your next rental without the hassle of searching</p>
                </v-sheet>
                <v-sheet class="pa-2 ma-2"></v-sheet>
                <v-sheet class="pa-2 ma-2">
                    <v-text-field class="text-input-yellow" variant = "solo" style="position:relative; color: yellow;"
                        label="Your email"
                        hide-details="auto"
                        >
                        <v-btn class="rounded-pill" style="position:absolute; top: 10px; left: 70%;"><h6 class = "button_text">Start trial</h6></v-btn>
                    </v-text-field>
                    <v-sheet class="pa-1 ma-1"></v-sheet>
                    <p style = "font-size: 60%;">
                        Try rentswipe for 3 days, no credit card required. By entering your email, 
                        you agree to  receive marketing emails from Rentswipe.
                    </p>
                </v-sheet>
            </v-col>
            <v-col>
                <v-sheet class="pa-2 ma-2">
                    <div id = "main-section">
                        <img src = "https://i.imgur.com/rA9TZap.png" style="width: 90%; height: 90%;"/>
                    </div>
                </v-sheet>
            </v-col>
        </v-row>
        
    </div>
</template>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@700&display=swap');
  @font-face {
    font-family: 'Raleway';
    src: url('https://fonts.googleapis.com/css2?family=Raleway:wght@700&display=swap') format('truetype');
  }
  
  h1 {
    font-family: 'Raleway';
  }

  .text-input-yellow .v-text-field__slot input {
   color: #00f !important;
}

</style>