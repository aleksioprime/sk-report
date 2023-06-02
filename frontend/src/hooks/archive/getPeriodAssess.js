import { ref, onMounted, computed } from 'vue'
import { axiosAPI } from '@/axios'

export function getPeriodAssess() {
  const periodAssess = ref([]);
  const getPeriodAssessData = async (data) => {
    const config = {
      params: {
        student: data.student || null,
        period: data.period || null,
        subject: data.subject || null,
        year: data.year || null,
      }
    }
    await axiosAPI.get(`/assessment/periodassess`).then((response) => {
      console.log("Загрузка оценок за период")
      periodAssess.value = response.data;
      console.log(periodAssess.value)
    });
  };
  return {
    periodAssess, getPeriodAssessData
  }
}

export function getStudents() {
  const students = ref([]);
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
  const getStudentsData = async (data) => {
    const config = {
      params: {
        year: data.year || null,
        period: data.period || null,
        subject: data.subject || null,
      }
    }
    console.log(config)
    await axiosAPI.get('/assessment/student', config).then((response) => {
      students.value = response.data;
      students.value.forEach((item) => {
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
      console.log("Студенты: ", students.value)
    });
  };
  return {
    students, calcFinalCriteriaMarks, getStudentsData
  }
}

export function getSumWork() {
  const sumWorks = ref([]);
  const getSumWorkData = async (data) => {
    const config = {
      params: {
        teacher: data.teacher || null,
        period: data.period || null,
        year: data.year || null,
        subject: data.subject || null,
      }
    }
    await axiosAPI.get('/assessment/sumwork', config).then((response) => {
      console.log("Загрузка итоговых работ")
      sumWorks.value = response.data;
      console.log(sumWorks.value)
    });
  };
  return {
    sumWorks, getSumWorkData
  }
}

export function getGroupedArray() {
  function groupedArrayData(array, fields) {
    let groupedObject = array.reduce((acc, obj) => {
      let objField = obj
      for (const field of fields) {
        objField = objField[field];
      }
      const property = objField.id;
      acc[property] = acc[property] || [];
      acc[property].push(obj);
      return acc;
    }, {});
    return groupedObject;
  }
  return {
    groupedArrayData
  }
}

export function getAssessmentJournal() {
  const currentPeriod = ref({});
  const currentSubject = ref({ group_ib: {} });
  const currentGroup = ref({});
  const getAssssmentJournalData = async (data) => {
    const config = {
      params: {
        period: data.period || null,
        year: data.year || null,
        subject: data.subject || null,
      }
    }
    await axiosAPI.get('/assessment/journal', config).then((response) => {
      console.log("Загрузка данных для журнала")
      currentPeriod.value = response.data.period;
      currentSubject.value = response.data.subject;
      currentGroup.value = response.data.group;
      console.log(response.data)
    });
  };
  return {
    currentPeriod, currentSubject, currentGroup, getAssssmentJournalData
  }
}

export function filterStudentsByGroup(students) {
  const queryGroup = ref(null);
  console.log(students.value)
  const filteredStudentsByGroup = computed(() => {
    if (queryGroup.value) {
      return students.value.filter(item => item.groups.map(item => item.id).includes(queryGroup.value));
    } else {
      return students.value
    }
  });
  return {
    queryGroup, filteredStudentsByGroup
  }
};