import { ref, onMounted, computed } from 'vue'
import { axiosAPI } from '@/axios'

export function getAssessmentJournal() {
  const currentPeriod = ref({});
  const currentSubject = ref({ group_ib: {} });
  const currentGroup = ref({ mentor: { user: {} }, class_year: {} });
  const currentClassYear = ref({});
  const fetchGetAssessmentJournal = async (data) => {
    const config = {
      params: {
        period: data.period || null,
        group: data.group || null,
        subject: data.subject || null,
      }
    }
    await axiosAPI.get('/assessment/journal', config).then((response) => {
      console.log("Загрузка данных для журнала")
      currentPeriod.value = response.data.period;
      currentSubject.value = response.data.subject;
      currentGroup.value = response.data.group;
      currentClassYear.value = response.data.class_year;
      console.log(response.data)
    });
  };
  return {
    currentPeriod, currentSubject, currentGroup, currentClassYear, fetchGetAssessmentJournal
  }
}

export function getSummativeWork() {
  const summativeWorks = ref([]);
  const fetchGetSummativeWork = async (data) => {
    const config = {
      params: {
        teacher: data.teacher || null,
        period: data.period || null,
        group: data.group || null,
        subject: data.subject || null,
      }
    }
    await axiosAPI.get('/assessment/sumwork', config).then((response) => {
      console.log("Загрузка итоговых работ")
      summativeWorks.value = response.data;
      console.log(summativeWorks.value)
    });
  };
  return {
    summativeWorks, fetchGetSummativeWork
  }
}

export function getStudentsAssessment() {
  const studentsAssessment = ref([]);
  const isStudentsAssessmentLoading = ref(true);
  const getCriterionMarkForStudent = (student, letter) => {
    const marks = student.workgroups.map(item => {
      const list_ = item.criteria_marks.filter(cm => cm.criterion.letter == letter).map(cm => cm.mark)
      return list_.toString()
    })
    return marks.filter(item => item).map(item => Number(item))
  }
  const getAverage = (numbers) => {
    if (numbers.length) {
      const sum = numbers.reduce((acc, number) => acc + number, 0);
      const length = numbers.length;
      return Math.round(sum / length);
    }
    return 0;
  }
  const calcSumCriteriaMarks = (listAverageMarks) => {
    const sumMarks = listAverageMarks.reduce((acc, number) => acc + number, 0);
    return sumMarks
  }
  const calcNumCriteriaMarks = (listAverageMarks) => {
    const sumAll = listAverageMarks.filter(item => item != 0).length;
    return sumAll
  }
  const calcFinalCriteriaMarks = (sumMarks, numMarks) => {
    const grades = { 1: [3, 5, 7], 2: [6, 10, 14], 3: [8, 14, 20], 4: [11, 19, 28] };
    if (!numMarks) {
      return '-'
    } else if (sumMarks >= grades[numMarks][2]) {
      return 5
    } else if (sumMarks < grades[numMarks][2] && sumMarks >= grades[numMarks][1]) {
      return 4
    } else if (sumMarks < grades[numMarks][1] && sumMarks >= grades[numMarks][0]) {
      return 3
    } else if (sumMarks < grades[numMarks][0] && sumMarks > 0) {
      return 2
    } else {
      return '-'
    }
  }
  const roundMark = (mark) => {
    if (mark) {
      return +mark.toFixed(2);
    }
    return 0;
  }
  const fetchGetStudentsAssessment = async (data) => {
    const config = {
      params: {
        group: data.group || null,
        class_year: data.class_year || null,
        period: data.period || null,
        subject: data.subject || null,
      }
    }
    isStudentsAssessmentLoading.value = true;
    await axiosAPI.get('/assessment/student', config).then((response) => {
      studentsAssessment.value = response.data;
      console.log("Студенты (чистые данные): ", response.data)
      studentsAssessment.value.forEach((item) => {
        item.calcCriteriaA = getCriterionMarkForStudent(item, 'A');
        item.calcCriteriaB = getCriterionMarkForStudent(item, 'B');
        item.calcCriteriaC = getCriterionMarkForStudent(item, 'C');
        item.calcCriteriaD = getCriterionMarkForStudent(item, 'D');
        const listMarks = [item.calcCriteriaA, item.calcCriteriaB, item.calcCriteriaC, item.calcCriteriaD];
        const listAverageMarks = listMarks.map(item => getAverage(item));
        item.sumCriteria = calcSumCriteriaMarks(listAverageMarks);
        item.allCriteria = calcNumCriteriaMarks(listAverageMarks) * 8;
        item.criteriaFinalMark = calcFinalCriteriaMarks(item.sumCriteria, calcNumCriteriaMarks(listAverageMarks));
        item.formativeMark = 0;
        item.finalGrade = roundMark(item.criteriaFinalMark * 0.6 + item.formativeMark * 0.4);
      })
      console.log("Студенты: ", studentsAssessment.value)
    }).finally(() => {
      isStudentsAssessmentLoading.value = false;
    });
  };
  return {
    studentsAssessment, calcFinalCriteriaMarks, isStudentsAssessmentLoading, fetchGetStudentsAssessment
  }
}