<template>
  <div class="module-container">
    <h3>Saque</h3>
    <form @submit.prevent="deposit">
      <label for="amount">Valor</label>
      <input type="number" name="amount" id="amount" v-model="amount" :disabled="isAccountLocked">

      <input type="submit" value="Sacar" :disabled="isAccountLocked">
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'AccountWithdrawal',
  emits: ['updateBalance'],
  data() {
    return {
      accountId: 0,
      amount: 0
    }
  },
  props: {
    isAccountLocked: {
      type: Boolean,
      default: false
    }
  },
  mounted() {
    this.accountId = JSON.parse(
      String(localStorage.getItem('user_account'))
    ).id;
  },
  methods: {
    deposit() {
      let amount = this.amount;
      let account_id = this.accountId;
      axios.post('http://localhost:5000/withdrawal', {
        amount: amount,
        account_id: account_id
      })
        .then((response) => {
          this.$emit('updateBalance');
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  }
});
</script>

<style scoped>
label {
  padding-top: 0;
}
</style>