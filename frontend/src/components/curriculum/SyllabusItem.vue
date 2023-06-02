<template>
  <div class="plan-item area">
    <div class="subject-title">
      <h4>{{ subject.name_rus }}&nbsp;(<span v-if="subject.group_ib">{{ subject.group_ib.program.toUpperCase() }}</span><span v-else>ФГОС</span>)</h4>
      <div v-if="subject.group_fgos">{{ subject.group_fgos.type }}: {{ subject.group_fgos.name_rus }}</div>
    </div>
    <div class="subject-hours">
      <div v-for="sb in dataSubjects" :key="sb.id" class="subject-hours-item" :class="{ 'editable-item': editableHour == sb.id }">
        <div><span v-for="year, index in sb.years" :key="year.id">{{ year.year_rus }}<span v-if="++index !== sb.years.length">,&nbsp;</span></span> класс:</div>
        <div>{{ getWordHour(sb.hours) }}</div>
        <button class="icon icon-del" @click="handleDelete(sb)" v-if="editableHour != sb.id"></button>
      </div>
    </div>
    <slot name="form"></slot>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { getGroupedArray } from "@/hooks/extra/extraFeatures";

export default {
  name: 'SyllabusItem',
  components: {
  },
  props: {
    subject: {
      type: Object,
      default: {}
    },
    dataSubjects: {
      type: Array,
      default: [],
    },
    editableHour: {
      type: Number,
      default: null,
    }
  },
  setup(props) {
    const { groupedArrayData } = getGroupedArray();
    return {
      groupedArrayData
    }
  },
  data() {
    return {

    }
  },
  methods: {
    handleDelete(sb) {
      this.$emit('deleteItem', sb);
      this.$emit('update:editableHour', Number(sb.id));
    },
    getWordHour(count) {
      let value = Math.abs(count) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${count} часов`;
      if (number > 1 && number < 5) return `${count} часа`;
      if (number == 1) return `${count} час`;
      return `${count} часов`;
    },
  },
  computed: {
    // подключение переменной авторизированного пользователя из store
    ...mapGetters(['authUser', 'isAdmin']),
  }
}
</script>

<style scoped>

.subject-title {
  margin: 10px 0;
}

.subject-hours {
  display: flex;
  gap: 5px;
}

.subject-hours-item {
  display: flex;
  column-gap: 5px;
  flex-direction: column;
  padding: 5px 10px;
  border: 1px solid #674A9E;
  border-radius: 5px;
  max-width: 130px;
  width: 100%;
  position: relative;
}
.icon {
  position: absolute;
  right: 5px;
  top: 5px;
  width: 20px;
  height: 20px;
}
.editable-item {
  background: #674A9E;
  color: #fff;
}
</style>