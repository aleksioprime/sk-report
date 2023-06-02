<template>
  <div class="sumworks-item">
    <div class="title selected">
      <div class="text"><h4>{{ sumwork.title }}</h4></div>
      <div class="tools">
        <div class="icon icon-edit" @click="$emit('editWork', sumwork)"></div>
        <div class="icon icon-del" @click="$emit('deleteWork', sumwork)"></div>
      </div>
    </div>
    <div class="teacher">Учитель:&nbsp;{{ sumwork.teacher.user.last_name }} {{ sumwork.teacher.user.first_name }} {{ sumwork.teacher.user.middle_name }}</div>
    <div class="unit">
      <div>Юнит:&nbsp;
        <a href="#" @click="$router.push(`/myp/${sumwork.unit.id}`)">{{ sumwork.unit.title }}</a> 
        <span v-if="sumwork.unit.interdisciplinary" class="badge rounded-pill text-bg-primary me-1">МДП<br></span>
      </div>
    </div>
    
    <div class="assessment">
      <div v-if="sumwork.groups.length" class="assessment-groups">
        <div class="group-title">Журналы оценок:</div>
        <div class="group-wrapper">
          <div class="group" v-for="gr in sumwork.groups" :key="gr.id" @click="$router.push(`/assessment/sumwork/${gr.id}`)">
            <div class="group-name">{{ gr.group.class_year.year_rus }}{{ gr.group.letter }} класс</div>
            <div class="group-date">{{ new Date(gr.date).toLocaleDateString() }}</div>
          </div>
        </div>
      </div>
      <div v-else class="assessment-groups">Не выбраны классы</div>
      <div class="assessment-criteria">
        <div class="criteria-title">Критерии оценки:</div>
        <div class="criteria-wrapper">
          <div class="criteria-item" :class="classCriteria(cr.letter)" v-for="cr in sumwork.criteria" :key="cr.id">{{ cr.letter }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    sumwork: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {

    }
  },
  methods: {
    classCriteria(letter) {
      if (letter.toLowerCase() == 'a') {
        return 'criterion-a'
      } else if (letter.toLowerCase() == 'b') {
        return 'criterion-b'
      } else if (letter.toLowerCase() == 'c') {
        return 'criterion-c'
      } else {
        return 'criterion-d'
      }
    },
  }
}
</script>

<style scoped>
.sumworks-item {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid var(--bs-secondary);
  border-radius: 10px;
}
.sumworks-item .title {
  display: flex;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
}
.sumworks-item .title .text h4 {
  margin-bottom: 0;
  text-transform: uppercase;
}
.sumworks-item .tools {
  display: flex;
  margin-left: auto;
}
.sumworks-item .tools .btn {
  border: none;
  min-width: 25px;
  min-height: 25px;
  cursor: pointer;
}

.sumworks-item .unit {
  margin-bottom: 10px;
}

.sumworks-item .assessment {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}
.sumworks-item .assessment-criteria {
  flex-basis: 40%;
}
.sumworks-item .assessment-groups {
  flex-basis: 60%;
}
.sumworks-item .criteria-wrapper {
  display: flex;
  justify-content: flex-start;
  row-gap: 5px;
  column-gap: 5px;
}
.sumworks-item .criteria-title {
  margin-bottom: 10px;
}
.criteria-item {
  margin-top: 0;
}
.sumworks-item .assessment .group-wrapper {
  display: flex;
  flex-wrap: wrap;
  padding-bottom: 5px;
  row-gap: 5px;
  column-gap: 5px;
}
.sumworks-item .assessment .group {
  padding: 5px 15px;
  text-align: center;
  border: 1px solid var(--my-focus);
  border-radius: 10px;
  cursor: pointer;
}
.sumworks-item .assessment .group:hover {
  transition: 0.5s;
  background: var(--my-focus);
  color: #000;
}
.sumworks-item .group-title {
  margin-bottom: 10px;
}
.sumworks-item .group-name {
  font-weight: 700;
}
.sumworks-empty 
{
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 30vh;
}

@media screen and (max-width: 540px) {
  
}

</style>