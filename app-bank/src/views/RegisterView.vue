<template>
  <div class="form-container">
    <div class="form-container-inner">
      <h1>Registrar</h1>
      <form @submit.prevent="register">
        <label for="name">Nome</label>
        <input type="text" name="name" id="name" v-model="name">

        <label for="cpf">CPF</label>
        <input type="text" name="cpf" id="cpf" v-model="cpf" @change="changeRegistry()" v-maska
          data-maska="###.###.###-##">

        <label for="birthdate">Data de Nascimento</label>
        <input type="date" name="birthdate" id="birthdate" v-model="birthdate">

        <input type="submit" value="Enviar">
      </form>
      <div>
        Já possui conta?
        <router-link to="/login">
          Entrar
        </router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'RegisterView',
  data() {
    return {
      name: '',
      cpf: '',
      registryToSend: '',
      birthdate: ''
    }
  },
  methods: {
    register() {
      let name = this.name;
      let cpf = this.registryToSend;
      let birthdate = `${this.birthdate} 03:00:00`

      axios.post('http://localhost:5000/person', {
        name: name,
        cpf: cpf,
        birthdate: birthdate
      })
        .then((response) => {
          this.$router.push('/login');
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    changeRegistry() {
      this.registryToSend = this.cpf.replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, "");
    }
  }
});
</script>

<style>

</style>