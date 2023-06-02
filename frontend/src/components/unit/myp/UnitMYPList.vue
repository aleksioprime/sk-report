<template>
  <div v-if="units.length > 0" ref="userlist">
    <!-- Список юнитов -->
    <transition-group name="unit-list">
      <div v-for="unit in units" :key="unit.id" class="unit-item area" :class="{ 'unit-item-interdisciplinary' : unit.interdisciplinary }">
        <div v-if="unit.interdisciplinary" class="unit-interdisciplinary" @click="$router.push(`/myp/idu/${unit.interdisciplinary.id}`)">
          <b>{{ unit.interdisciplinary.title }}</b>
          (<span v-for="(un, index) in unit.interdisciplinary.unitplan_myp" :key="un.id">
            {{ un.subject.name_rus }}<span v-if="++index !== unit.interdisciplinary.unitplan_myp.length">,&nbsp;</span>
          </span>)
        </div>
        <div class="unit-header selected" @click="$router.push(`/myp/${unit.id}`)">
          <div class="unit-title"><h4>{{ unit.title }}</h4></div>
          <small v-if="unit.subject && unit.class_year">
            {{ unit.subject.name_rus }}, {{ unit.class_year.year_ib }} {{ unit.class_year.program }} ({{ getHours(unit.hours) }})
          </small>
        </div>
        <div class="unit-concepts">
          <div v-for="kc in unit.key_concepts" :key="kc.id" class="unit-kc">{{ kc.name_eng }}</div>
          <div v-for="(rc, index) in unit.related_concepts" :key="rc.id" class="unit-rc">{{ rc.name_eng }}
            <span v-if="++index !== unit.related_concepts.length">,&nbsp;</span>
          </div>
        </div>
        <div class="unit-gcontext" v-if="unit.global_context">
          {{ unit.global_context.name_eng }}
          (<span v-for="(exp, index) in unit.explorations" :key="exp.id" class="unit-rc">
            {{ exp.name_eng }}<span v-if="++index !== unit.explorations.length">,&nbsp;</span></span>)
        </div>
        <div class="unit-soi" v-if="unit.statement_inquiry" v-html="unit.statement_inquiry">
        </div>
        <div class="unit-atl" v-if="unit.atl_mapping.length">
          <div class="me-2">ATL: </div>
          <div v-for="atl, index in unit.atl_mapping" :key="atl.id" class="atl-item">
            {{atl.atl.cluster.name_eng }}<span v-if="++index !== unit.atl_mapping.length">,&nbsp;</span>
          </div>
        </div>
        <div class="unit-footer">
          <div class="unit-criteria">
            <div v-for="cr in unit.criteria" :key="cr.id" class="criteria-item" :class="classCriteria(cr.letter)">
              {{ cr.letter }}
            </div>
          </div>
          <div class="unit-authors">
            <div v-for="author in unit.authors" :key="author.id" class="authors-item">{{ author.last_name }} {{ author.first_name }} {{ author.middle_name }}</div>
          </div>
        </div>
        <div class="unit-progress">
          <div class="me-2">Заполнение: </div>
          <div class="progress w-100" style="height: 15px;">
            <div class="progress-bar" role="progressbar" :style="`width: ${unit.fullness}%`" :aria-valuenow="unit.fullness" aria-valuemin="0" aria-valuemax="100">{{ unit.fullness }}%</div>
          </div>
        </div>
        
      </div>
    </transition-group>
    <!-- Нумерация страниц -->
    <base-pagination :total="totalPages" :current="currentPage" :range="4" @change="nextPage" />
  </div>
  <div v-else>
    Данных нет
  </div>
</template>

<script>

export default {
  name: 'UnitMYPList',
  props: {
    units: {
      type: Array,
      required: true,
      default: [],
    },
    totalPages: {
      type: Number,
      default: 1,
    },
    currentPage: {
      type: Number,
      default: 1,
    },
  },
  setup(props) {

    return {

    }
  },
  data() {
    return {

    }
  },
  methods: {
    nextPage(page) {
      this.$emit('changePage', page)
    },
    containsKey(obj, key) { return Object.keys(obj).includes(key) },
    hasSubject(unit) { return this.containsKey(unit, 'subject') },
    hasClassYear(unit) { return this.containsKey(unit, 'class_year') },
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
    getHours(hours) {
      let value = Math.abs(hours) % 100;
      let number = value % 10;
      if (value > 10 && value < 20) return `${hours} часов`;
      if (number > 1 && number < 5) return `${hours} часа`;
      if (number == 1) return `${hours} час`;
      return `${hours} часов`;
    }
  },
  computed: {
    
  },
  mounted() {

  },
}
</script>
  
<style scoped>
.unit-interdisciplinary {
  border: 1px solid var(--my-gymnasium);
  background: #fff;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
  color: var(--my-gymnasium);
  margin-top: -40px;
  text-transform: uppercase;
}

.unit-interdisciplinary:hover {
  transition: 0.5s;
  background: var(--my-gymnasium);
  color: #fff;
  cursor: pointer;
}
.unit-item {
  border-radius: 10px;
  margin: 20px 0;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.unit-item-interdisciplinary  {
  margin-top: 40px;
}

.unit-header {
  padding: 5px 10px;
  border-radius: 10px;
  margin-bottom: 10px;
}
.unit-header:hover {
  cursor: pointer;
}

.unit-title {
  font-weight: 700;
  text-transform: uppercase;
}

.unit-concepts {
  display: flex;
  flex-wrap: wrap;
}

.unit-kc {
  margin-right: 10px;
  text-decoration: underline;
}

.unit-soi {
  position: relative;
  margin-left: 20px;
  color: #333334;
  padding: 10px 10px 5px 10px;
  position: relative;
}

.unit-soi:before {
  content: "\201C";
  font-family: serif;
  position: absolute;
  left: -20px;
  top: -5px;
  color: #BCBCBC;
  font-size: 50px;
  text-shadow: 1px 2px 0 white;
}

.unit-soi p {
  margin-bottom: 0px;
}

.unit-criteria {
  display: flex;
  max-width: 300px;
  column-gap: 5px;
  margin: 10px 0;
}

.criteria-item {
  margin-top: 0;
  border-radius: 5px;
  padding: 5px;
  width: 40px;
  text-align: center;
  font-weight: 700;
}

.unit-atl {
  border: 1px solid #dee2e6;
  border-left: none;
  border-right: none;
  padding: 5px;
  display: flex;
  flex-wrap: wrap;
}
.unit-footer {
  display: flex;
  align-items: center;
}
.unit-authors {
  margin-left: auto;
  font-style: italic;
  padding-left: 10px;
}
.unit-progress {
  display: flex;
  align-items: center;
}
</style>