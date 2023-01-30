<template>
  <div>
    <form @submit.prevent="uploadFileImport">
      <label for="importFile" class="form-label">Импорт пользователей из файла в формате <b>xlsx</b></label>
      <div class="row">
        <div class="col-md my-2">
          <input class="form-control" type="file" id="importFile" ref="excelUser" @change="handleFileUpload" />
        </div>
        <div class="col-md-3 my-2">
          <button class="btn btn-primary" type="submit" :disabled="!file">Загрузить</button>
        </div>
      </div>
    </form>
    <div class="table-wrapper">
      <table class="table" v-if="applicantUsers.length">
        <thead>
          <tr>
            <th style>Пользователь</th>
            <th>ФИО</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user, index in applicantUsers" :key="index" :class="[checkUser(user.username) ? 'success' : 'error']">
            <td>{{ user.username }}<br>{{ user.email }}</td>
            <td>{{ user.last_name }}<br>{{ user.first_name }}<br>{{ user.middle_name }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else class="p-2">
        Загрузите данные пользователей
      </div>
    </div>
  </div>
</template>

<script>
import { toRefs } from 'vue'

export default {
  props: {
    modelValue: { type: Array },
  },
  setup() {
    return { };
  },
  data() {
    return {
      file: null,
      applicantUsers: [],
      validatedUsers: [],
    }
  },
  methods: {
    handleFileUpload() {
      [this.file] = this.$refs.excelUser.files;
    },
    uploadFileImport() {
      const formData = new FormData();
      formData.append('import', this.file);
      this.axios.post('/user/load', formData)
        .then((response) => {
          console.log(response);
          if (response.data.applicant_users && response.data.validated_users) {
            this.applicantUsers = response.data.applicant_users;
            this.validatedUsers = response.data.validated_users;
            this.$emit('update:modelValue', [ ...this.validatedUsers]);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    checkUser(value) {

      return this.validatedUsers.map(item => item.username).includes(value)
    }
  },
  mounted() {
    // console.log(this.$cookies.get('csrftoken'));
  },
  watch: {
    
  }
}
</script>

<style scoped>
.table-wrapper {
  overflow-y: scroll;
  height: 50vh;
  border: 1px solid #28a8a8;
  margin-top: 10px;
}
.success {
  background-color: aquamarine;
}
.error {
  background-color: rgb(179, 55, 55);
  color: white;
}
</style>