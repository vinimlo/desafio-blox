<template>
  <div class="module-container">
    <h3>
      Saldo
      <button class="reload-btn" @click="getBalance()">
        <span class="icon">
          <i class="fas fa-rotate-right"></i>
        </span>
      </button>
    </h3>

    <strong>
      {{ balance }}
    </strong>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'AccountBalance',
  data() {
    return {
      accountId: 0,
      balance: 0
    }
  },
  mounted() {
    this.accountId = JSON.parse(
      String(localStorage.getItem('user_account'))
    ).id
    this.getBalance()
  },
  methods: {
    getBalance() {
      axios.get(`http://localhost:5000/balance/${this.accountId}`)
        .then((response: any) => {
          this.balance = response.data.balance
        });
    }
  }
});
</script>

<style>

</style>