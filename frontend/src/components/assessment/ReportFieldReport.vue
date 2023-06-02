<template>
  <div class="unit-field">
    <div class="field-title">
      <div class="field-label">Отчёт по студенту</div>
      <button v-if="editable && !editMode" class="field-btn-edit" @click="editField">Редактировать</button>
    </div>
    <div class="field-data" :class="{ 'field-editing': editMode }">
      <transition name="slide-fade">
        <div v-if="!editMode">
          <div v-html="dataField.text"></div> 
        </div>
        <div v-else>
          <div class="field-description">Введите описание</div>
          <div v-if="report.subject && report.subject.group_ib">
            <div>Достижения студента по описаниям из гайда предметной группы <b>{{ report.subject.group_ib.name_eng }}</b></div>
            <div class="achievement-description" v-if="report.achievements.length">
              <span v-for="achieve in report.achievements" :key="achieve.id" class="description-item">
                <span @click="translateSelected" v-if="achieve.achievement" class="popup">The student {{ achieve.achievement_description }}.&nbsp;<span class="popuptext"></span></span>
                <span @click="translateSelected" class="popup" v-else>The student failed to do {{ achieve.objective_description }}.&nbsp;<span class="popuptext"></span></span>
              </span>
            </div>
            <div v-else  class="achievement-description">Не было выбрано ни одного достижения студента</div>
          </div>
          
          <div v-show="!reportLoading && tinyLoading">
              <editor api-key="j30bef5hr2ipfdbu7b9lww7t4oez2v6f27c94otp9to2j9mk"
              :init="{
                plugins: 'lists link wordcount autoresize',
                menubar: false,
                toolbar: 'removeformat | undo redo | bold italic | forecolor | alignleft aligncenter alignright alignjustify | bullist numlist ',
                setup: (ed) => {
                    ed.on('init', () => { tinyLoading = true });
                }
              }"
              model-events="change keydown blur focus paste" output-format="html" v-model="editData.text"/>
          </div>
          <div v-if="reportLoading || !tinyLoading" class="loader">
            <div class="lds-spinner">
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
              <div></div>
            </div>
          </div>
          <div class="field-buttons">
            <!-- Генератор отключен, так как превышена квота -->
            <!-- <button class="field-btn-generate" v-if="generate" @click="generateField">Сгенерировать</button> -->
            <button class="field-btn-done" @click="saveField">Сохранить</button>
            <button class="field-btn-cancel" @click="cancelField">Отмена</button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios'
import Editor from '@tinymce/tinymce-vue';
import { getChatGPTReport } from "@/hooks/assess/useGenerateReport";

export default {
  name: 'ReportFieldText',
  components: {
    'editor': Editor
  },
  props: {
    report: { 
      type: Object, 
      default: {}
    },
    dataField: { type: Object, default: {} },
    generate: { type: Boolean, default: false },
    editable: { type: Boolean, default: false },
  },
  setup(props) {
    const { generatedGPTText, isGPTTextLoading, fetchChatGPTReport } = getChatGPTReport();
    return {
      generatedGPTText, isGPTTextLoading, fetchChatGPTReport
    }
  },
  data() {
    return {
      editMode: false,
      editData: {},
      reportLoading: false,
      tinyLoading: false,
    }
  },
  methods: {
    testTinyMCE() {
      console.log('testing')
    },
    saveField() {
      this.editMode = false;
      this.$emit('save', this.editData)
    },
    cancelField() {
      this.editMode = false;
    },
    editField() {
      this.editMode = true;
      this.editData.text = this.dataField.text;
    },
    async generateField() {
      let phraseList = []
      this.report.achievements.forEach((item) => {
        if (item.achievement) {
          phraseList.push(`The student ${item.achievement_description}`)
        } else {
          phraseList.push(`The student failed to do ${item.objective_description}`)
        }
      })
      if (this.report) {
        const data = {
          name: this.report.student.user.first_name,
          subject: this.report.subject.name_rus,
          text: phraseList.join('. '),
          final_grade: this.report.final_grade,
        }
        this.reportLoading = true;
        await this.axios.post('/generate/report', data).then((response) => {
          console.log(response.data)
          if (response.data.result != 'failed' ) {
            this.editData.text = response.data.text;
          }
          this.reportLoading = false;
        });
      } else {
        console.log('Нет данных')
      }
    },
    // async translateGoogle(text) {
    //   const API_KEY = 'AIzaSyCBFVvqme-1gwz5bJhE59jsFRicX5Ao93s'
    //   let res = await axios.post(`https://translation.googleapis.com/language/translate/v2?key=${API_KEY}`, { q: text, target: "ru" });
    //   let translation = res.data.data.translations[0].translatedText;
    //   return translation;
    // },
    // async translateYandex(text) {
    //   const idCat = 'b1g77n8c28300fhesa8s';
    //   const IAM = 't1.9euelZqVkImUmInPmsuelIrNnJWJkO3rnpWamZPMmpiUi47Gx5vPj4vLjovl8_c0ZmZc-e9BPEAA_t3z93QUZFz570E8QAD-.-6-IJaKpb16RsQy7ME-6SZ5tyvYagxKyE0dsnmktb9_sVEfRsXiAmrfLV0j75fFgwyFlczToTJA1Ol5ydAmtCw'
    //   const config = {
    //     headers: {
    //       'Content-Type': 'application/json',
    //       'Authorization': `Bearer ${IAM}`
    //     },
    //     body: {
    //       "targetLanguageCode": 'ru',
    //       "texts": text,
    //       "folderId": idCat,
    //     }
    //   }
    //   let res = await axios.post(`https://translate.api.cloud.yandex.net/translate/v2/translate`, config);
    //   let translation = res.data.ranslations;
    //   return translation;
    // },
    async translateSelected(event) {
      // TODO: Сделать автоподмену name_rus, если есть, иначе перевод google
      const popup = event.target.lastChild;
      if (event.target.classList.contains('show')) {
        event.target.classList.remove('show')
        event.target.textContent = ''
        return
      }
      console.log(popup)
      const data = {
        text: event.target.textContent,
        language: 'ru',
      }
      await this.axios.post('/translate', data).then((response) => {
        console.log(response.data)
        if (response.data.result != 'failed' ) {
          popup.textContent = response.data.text
          popup.classList.toggle('show')
        }
      });
    }
  },
}
</script>
<style scoped>
@import '@/assets/css/spinner.css';
.loader {
  height: 200px;
}
.achievement-description {
  font-size: 0.8em;
  padding: 10px;
}
.field-btn-generate {
  border: none;
  border-radius: 5px;
  background-color: #33cc40;
  color: #fff;
  padding: 3px 8px;
  margin-left: auto;
  font-size: 0.8em;
}
.description-item:hover {
  background: var(--my-focus);
  cursor: pointer;
}

/* Popup container */
.popup {
  position: relative;
  cursor: pointer;
}

/* The actual popup (appears on top) */
.popup .popuptext {
  visibility: hidden;
  width: 160px;
  background-color: var(--my-focus);
  color: #000;
  text-align: center;
  border-radius: 6px;
  padding: 10px;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  margin-left: -80px;
}

/* Popup arrow */
.popup .popuptext::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: var(--my-focus) transparent transparent transparent;
}

/* Toggle this class when clicking on the popup container (hide and show the popup) */
.popup .show {
  visibility: visible;
  -webkit-animation: fadeIn 1s;
  animation: fadeIn 1s
}

/* Add animation (fade in the popup) */
@-webkit-keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}

@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity:1 ;}
}
</style>