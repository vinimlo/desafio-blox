<template>
  <div class="module-container">
    <h3>
      Extrato
      <button class="reload-btn" @click="getTransactions(currentPage)">
        <span class="icon">
          <i class="fas fa-rotate-right"></i>
        </span>
      </button>
    </h3>

    <table>
      <tr id="table-header">
        <td>Operação</td>
        <td>Valor</td>
        <td>Data</td>
      </tr>
      <tr v-for="(transaction, index) in transactions" :key="index">
        <td>
          <small v-if="transaction.amount > 0" class="deposit-label">
            Depósito
          </small>
          <small v-if="transaction.amount < 0" class="withdrawal-label">
            Saque
          </small>
        </td>
        <td>
          R$ {{ String(Number(transaction.amount).toFixed(2)).replace('.', ',') }}
        </td>
        <td>
          {{ formatDate(String(transaction.date_created)) }}
        </td>
      </tr>
    </table>
    <div id="btn-container">
      <button :disabled="currentPage == 1" @click="getTransactions(currentPage, -1)">
        &lt;
      </button>
      <span>
        {{ currentPage }} / {{ pagesNumber }}
      </span>
      <button :disabled="currentPage == pagesNumber" @click="getTransactions(currentPage, +1)">
        &gt;
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import ITransaction from '@/interfaces/ITransaction';

export default defineComponent({
  name: 'AccountTransactions',
  data() {
    return {
      transactions: [] as Array<ITransaction>,
      currentPage: 1,
      pagesNumber: 1,
      resultsPage: 10,
      accountId: 0
    }
  },
  mounted() {
    this.accountId = JSON.parse(
      String(localStorage.getItem('user_account'))
    ).id;
    this.getTransactions(this.currentPage);
  },
  methods: {
    getTransactions(page: number, pagination = 0) {
      if (pagination !== 0) page += pagination;

      axios.get(`http://localhost:5000/transactions/${this.accountId}?page=${page}`)
        .then((response: any) => {
          this.currentPage = response.data.pagination.page
          this.pagesNumber = response.data.pagination.pages
          this.resultsPage = response.data.pagination.per_page
          this.transactions = response.data.transactions;
        });
    },
    formatDate(date: string): string {
      let newDate = new Date(date);

      let hour = ('00' + newDate.getHours()).slice(-2);
      let minutes = ('00' + newDate.getMinutes()).slice(-2);
      let formattedDate = `${newDate.toLocaleDateString()} ${hour}:${minutes}`;
      return formattedDate;
    }
  }
});
</script>

<style scoped>
table {
  background-color: rgba(0, 0, 0, 0.3);
  color: #FAFAFA;
  width: 80%;
  margin: 0 auto;
  display: table;
  border-radius: 8px;
}

tr {
  width: 100%;
}

td {
  width: 33%;
}

#table-header {
  font-weight: 700;
}

.deposit-label {
  color: #43A047;
}

.withdrawal-label {
  color: #F4511E;
}

#btn-container {
  margin: 15px auto;
}

#btn-container button {
  background: none;
  border: none;
  color: #FAFAFA;
  font-size: 1.3em;
  padding: 0 30px;
  cursor: pointer;
  font-weight: 900;
}

#btn-container button:disabled {
  color: rgba(255, 255, 255, 0.3);
}
</style>