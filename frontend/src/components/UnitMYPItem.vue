<template>
  <tr>
    <td>
      {{ unitplan.order }}
    </td>
    <td>
      <a class="title" href="#" @click="$router.push(`/unit/${unitplan.id}`)">{{ unitplan.title }}</a> ({{
          unitplan.hours
      }} часов)
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
        {{ unitplan.statement_inquiry }}
      </div>
      <div v-else>Нет данных</div>
    </td>
    <td>
      <span class="badge rounded-pill text-bg-primary me-1" v-for="cr in unitplan.criteria" :key="cr.id">{{ cr.letter
      }}</span>
    </td>
    <td>
      <ul v-if="unitplan.key_concepts.length > 0">
        <li v-for="atl in unitplan.atl_skills" :key="atl.id">{{ atl.name_eng }}</li>
        </ul>
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
    }
  },
  data() {
    return {
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