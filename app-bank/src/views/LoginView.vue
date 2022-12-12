<template>
  <div class="form-container">
    <div class="form-container-inner">
      <h1>Login</h1>
      <div v-if="shouldRegister">
        <h3>
          Você ainda não está registrado!
        </h3>
      </div>
      <form @submit.prevent="login">
        <label for="user-registry">CPF</label>
        <input type="text" name="user-registry" id="user-registry" @change="changeRegistry()" v-model="userRegistry"
          v-maska data-maska="###.###.###-##">
        <input type="submit" value="Entrar">
      </form>
      <div>
        Ainda não possui conta?
        <router-link to="/register">
          Registrar
        </router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { vMaska } from "maska"

export default defineComponent({
  name: 'LoginView',
  data() {
    return {
      userRegistry: '',
      registryToSend: '',
      shouldRegister: false
    }
  },
  methods: {
    login() {
      axios.get(`http://localhost:5000/search_account/${this.registryToSend}`)
        .then((response: any) => {
          let message = response.data.message;

          if (message) {
            switch (message) {
              case 'Person does not exist.':
                this.shouldRegister = true;
                break;
              case 'Account does not exist.':
                this.$router.push({
                  name: 'create-account',
                  params: { userRegistry: this.userRegistry }
                })
                break;
            }
          }
          else {
            localStorage.setItem('user_account', JSON.stringify(response.data));
            (this.$root as any).userIsLogged = true;
            (this.$root as any).username = JSON
              .parse(
                String(localStorage.getItem('user_account'))
              ).person_relation.name;
            this.$router.push('/');
          }
        });
    },
    changeRegistry() {
      this.registryToSend = this.userRegistry.replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, "");
    }
  }
});
</script>

<style>

</style>