<template>
  <tr>
    <td>
      {{ index }}
    </td>
    <td>
      <a class="title" :href="`/unit/${unitplan.id}`">{{ unitplan.title }}</a>
      ({{ unitplan.hours }} ч.)<br>
      <span v-if="checkInterdisciplinary" class="badge rounded-pill text-bg-primary me-1">МДП<br></span>
      <span v-for="(sb, i) in unitplan.subjects" :key="i">{{ sb.subject.name_rus }}<br></span>
      <a href="#" @click="$emit('export', unitplan)">Экспорт в word</a>
    </td>
    <td>
      <div v-if="unitplan.key_concepts.length > 0">
        <span class="key-concepts" v-for="kc in unitplan.key_concepts" :key="kc.id">{{ kc.name_eng }}</span><br>
        <span v-for="rc in unitplan.related_concepts" :key="rc.id">{{ rc.name_eng }}<br></span>
      </div>
      <div v-else>Нет данных</div>
    </td>
    <td>
      <div v-if="unitplan.global_context">
        <span class="global-context">{{ unitplan.global_context.name_eng }}</span><br>
        <span v-for="exp in unitplan.explorations" :key="exp.id">{{ exp.name_eng }}<br></span>
      </div>
      <div v-else>Нет данных</div>
    </td>
    <td>
      <div v-if="unitplan.statement_inquiry">
        <div v-html="unitplan.statement_inquiry"></div>
      </div>
      <div v-else>Нет данных</div>
    </td>
    <td>
      <div v-for="(value, field) in groupedField(unitplan.criteria, 'subject_group')" :key="field">
        <div v-if="checkInterdisciplinary && subjectGroupUnit.length > 0"><small>{{ subjectGroupUnit.find(item => item.id == field).name_eng }}</small></div>
        <span class="badge rounded-pill text-bg-primary me-1" v-for="cr in value" :key="cr.id">{{ cr.letter }}</span>
      </div>
    </td>
    <td>
      <div v-if="unitplan.atlmapping.length > 0">
        <div v-for="am in unitplan.atlmapping" :key="am.id">{{ am.atl.name_eng }}<br><b>{{ am.atl.cluster.name_eng }}</b></div>
      </div>
      <div v-else>Нет данных</div>
    </td>
  </tr>
</template>

<script>
export default {
  props: {
    unitplan: {
      type: Object,
      required: true,
    },
    index: { type: Number },
  },
  data() {
    return {
    }
  },
  methods: {
    groupedField(field, name) {
      let groupedObject = field.reduce((acc, obj) => {
        const property = obj[name].id;
        acc[property] = acc[property] || [];
        acc[property].push(obj);
        return acc;
      }, {});
      return groupedObject;
    },
  },
  computed: {
    subjectGroupUnit() {
      let objArray = this.unitplan.subjects.map(sb => sb.subject.group_ib);
      return [...new Map(objArray.map((item) => [item["id"], item])).values()];
    },
    checkInterdisciplinary() {
      return this.unitplan.subjects.length > 1;
    }
  },
}
</script>

<style scoped>
.title {
  font-weight: bold;
  color: rgb(32, 45, 102);
  text-decoration: none;
}

.key-concepts {
  font-weight: bold;
  color: rgb(12, 70, 10);
}

.global-context {
  font-weight: bold;
  color: rgb(12, 70, 10);
}
</style>