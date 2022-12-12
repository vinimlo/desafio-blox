<template>
  <div class="form-container">
    <div class="form-container-inner">
      <h1>Criar conta</h1>
      <div class="extra-info">
        <label for="name">Nome</label>
        <span id="name">{{ name }}</span>

        <label for="cpf">CPF</label>
        <span id="cpf">{{ cpf }}</span>

        <label for="birthdate">Data de Nascimento</label>
        <span id="birthdate">{{ birthdate }}</span>
      </div>
      <form @submit.prevent="createAccount">

        <label for="account-type">Tipo de conta</label>
        <select name="account-type" id="account-type" v-model="accountType">
          <option value="1">Conta Poupança</option>
          <option value="2">Conta Corrente</option>
        </select>

        <input type="submit" value="Criar">
      </form>

    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'CreateAccountView',
  props: {
    userRegistry: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      name: '',
      cpf: '',
      registryToSend: '',
      birthdate: '',
      accountType: 0,
      userId: 0
    }
  },
  mounted() {
    this.cpf = this.userRegistry;
    this.registryToSend = this.userRegistry.replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, "");
    axios.get(`http://localhost:5000/person/${this.registryToSend}`)
      .then((response: any) => {
        this.birthdate = response.data.birthdate.substring(0, 10);
        this.name = response.data.name;
        this.userId = response.data.id;
      });
  },
  methods: {
    createAccount() {
      let accountType = +this.accountType;
      let person_id = this.userId;

      axios.post('http://localhost:5000/account', {
        account_type: accountType,
        person_id: person_id
      })
        .then((response) => {
          localStorage.setItem('user_account', JSON.stringify(response.data));
          (this.$root as any).userIsLogged = true;
          (this.$root as any).username = JSON
            .parse(
              String(localStorage.getItem('user_account'))
            ).person_relation.name;
          this.$router.push('/');
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  }
});
</script>

<style>

</style>