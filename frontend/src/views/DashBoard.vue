<template>
  <div>
    <base-header>
      <template v-slot:header>Информационная панель</template>
    </base-header>
    <div class="area p-3">
      <h4>Здравствуйте, <span v-if="authUser">{{ authUser.first_name }}</span>!</h4>
      <div v-if="authUser && authUser.teacher">
        <div class="my-3">Вы находитесь в экспериментальной системе <b>Stream Report</b> Международной Гимназии Сколково</div>
        <div>Ваша должность: {{ authUser.teacher.position }}</div>
        <div v-if="authUser.teacher.groups.length">Вы наставник в классах: <span v-for="group, index in authUser.teacher.groups" :key="group.id"><b>{{ group.class_year }}{{ group.letter }}</b><span v-if="++index !== authUser.teacher.groups.length">,&nbsp;</span></span></div>
        <div v-if="authUser.teacher.psycho_groups.length">Вы психолог в классах: <span v-for="group, index in authUser.teacher.psycho_groups" :key="group.id"><b>{{ group.class_year }}{{ group.letter }}</b><span v-if="++index !== authUser.teacher.psycho_groups.length">,&nbsp;</span></span></div>
        <div v-if="workLoads.length">
          <div class="mt-2">В <b>{{currentStudyYear.name}}</b> учебном году вы преподаёте следующие предметы: </div>
          <ul>
            <li v-for="work in workLoads" :key="work.id">{{ work.subject_name }} в <span v-for="gr in work.groups" :key="gr.id">{{ gr.group_name }}</span> классах</li>
          </ul>
        </div>
        <div v-else>Вам в нагрузку не добавлены дисциплины</div>
        <div class="mt-3"><b>Stream Report</b> в настоящий момент находится в разработке, но некоторые функции уже доступны. Если вы обнаружили ошибки в работе программы, просим вас <a href="#" @click="showFeedback">оставить нам сообщение</a></div>
        <div class="mb-3" v-if="showForm">
          <textarea v-model="feedback.message" class="form-control mt-2" id="exampleFormControlTextarea1" rows="3"></textarea>
          <div class="d-flex">
            <button class="btn btn-primary my-2" @click="sendMessage">Отправить</button>
            <button class="btn btn-secondary my-2" @click="hideFeedback">Отмена</button>
          </div>
        </div>
        <div class="alert alert-success mt-4 text-center" role="alert" v-if="showSuccess && !showForm">
          Сообщение успешно отправлено!<br>
          <a href="#" @click="showFeedback">Отправить ещё сообщение</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { getWorkLoads } from "@/hooks/assess/useWorkLoad";
import { getStudyYears } from "@/hooks/assess/useStudyYear";

export default {
  name: 'DashBoard',
  setup(porps) {
    const { workLoads, fetchGetWorkLoads } = getWorkLoads();
    const { studyYears, currentStudyYear, fetchGetStudyYears } = getStudyYears();

    return {
      workLoads, fetchGetWorkLoads,
      studyYears, currentStudyYear, fetchGetStudyYears,
    }
  },
  data() {
    return {
      feedback: {},
      showForm: false,
      showSuccess: false,
    }
  },
  methods: {
    sendMessage() {
      this.feedback.name = `${this.authUser.last_name} ${this.authUser.first_name} ${this.authUser.middle_name}`
      this.feedback.email = this.authUser.email;
      if (this.feedback.message) {
        this.axios.post('/feedback', this.feedback).then((response) => {
          if (response.data.result == 'success') {
            this.feedback = {};
            this.showSuccess = true,
            this.showForm = false;
          }
          console.log('Сообщение отправлено', response.data);
        }).catch((error) => {
          console.log('Ошибка запроса: ', error);
        });
      }
    },
    hideFeedback() {
      this.showForm = false;
      this.feedback = {};
    },
    showFeedback() {
      this.showForm = true;
      this.showSuccess = false;
    },
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  },
  mounted() {
    if (this.authUser.teacher) {
      this.fetchGetStudyYears().finally(() => {
        this.fetchGetWorkLoads({ study_year: this.currentStudyYear.id, teacher: this.authUser.teacher.id});
      })
    }
  }
}
</script>

<style></style>