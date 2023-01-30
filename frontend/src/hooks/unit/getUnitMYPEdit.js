import { ref } from 'vue';
import { axiosAPI } from '@/axios'

export function getUnitView() {
	const unit = ref([]);
	const getUnitData = async (id) => {
		await axiosAPI.get('/unitplans/myp/' + id).then((response) => {
			unit.value = response.data;
		});
	};
	return {
		unit, getUnitData
	}
}

export function getTeachers() {
	const authors_list = ref([]);
	const getTeachersData = async () => {
		await axiosAPI.get('/teachers').then((response) => {
			authors_list.value = response.data;
		});
	};
	return {
		authors_list, getTeachersData
	}
}

export function getKeyConcepts() {
	const key_concepts_list = ref([]);
	const getKeyConceptsData = async () => {
		await axiosAPI.get('/kconcepts').then((response) => {
			key_concepts_list.value = response.data;
		});
	};
	return {
		key_concepts_list, getKeyConceptsData
	}
}

export function getRelatedConcepts() {
	const related_concepts_list = ref([]);
	const getRelatedConceptsData = async (subjects) => {
		const config = {
      params: {
			  subjects: subjects,
      }
		};
		await axiosAPI.get('/rconcepts', config).then((response) => {
			related_concepts_list.value = response.data;
		});
	};
	return {
		related_concepts_list, getRelatedConceptsData
	}
}

export function getGlobalContext() {
	const global_context_list = ref([]);
	const getGlobalContextData = async () => {
		await axiosAPI.get('gcontext').then((response) => {
			global_context_list.value = response.data;
		});
	};
	return {
		global_context_list, getGlobalContextData
	}
}

export function getExplorations() {
  const explorations_list = ref([]);
  const getExplorationsData = async (gcontext) => {
    const config = {
      params: {
			  gcontext: gcontext,
      }
		};
    await axiosAPI.get('/explorations', config).then((response) => {
        explorations_list.value = response.data;
    });
  };
  return {
    explorations_list, getExplorationsData
  }
}

export function getAims() {
  const aims_list = ref([]);
  const getAimsData = async (subjects, group) => {
    const config = {
      params: {
        subjects: subjects,
        group: group,
      }
    };
    await axiosAPI.get('/aims', config).then((response) => {
      aims_list.value = response.data;
    });
  };
  return {
    aims_list, getAimsData
  }
}

export function getCriteria() {
  const criteria_list = ref([]);
  const getCriteriaData = async (subjects, group) => {
    const config = {
      params: {
        subjects: subjects,
        group: group,
      }
    };
    await axiosAPI.get('/criteria', config).then((response) => {
      criteria_list.value = response.data;
    });
  };
  return {
    criteria_list, getCriteriaData
  }
}

export function getStrands() {
  const strands_list = ref([]);
  const getStrandsData = async (subjects, group, criteria) => {
    const config = {
      params: {
        subjects: subjects,
        criteria: criteria,
        group: group,
      }
    };
    await axiosAPI.get('/strands', config).then((response) => {
      strands_list.value = response.data;
    });
  };
  return {
    strands_list, getStrandsData
  }
}

export function getATLSkills() {
  const atlSkills = ref([]);
  const getATLSkillsData = async () => {
    await axiosAPI.get('/atlskills').then((response) => {
      atlSkills.value = response.data;
    });
  };
  return {
    atlSkills, getATLSkillsData
  }
}

export function getIBLearnerProfile() {
	const learner_profile_list = ref([]);
	const getIBLPData = async () => {
		await axiosAPI.get('/ibprofile').then((response) => {
			learner_profile_list.value = response.data;
		});
	};
	return {
		learner_profile_list, getIBLPData
	}
}

// export function getObjectives() {
//   const objectives_list = ref([]);
//   const getObjectivesData = async (subject, class_year, criteria) => {
//     const config = {
//       params: {
//         subject: subject,
//         class_year: class_year,
//         criteria: criteria,
//       }
//     };
//     await axiosAPI.get('/objectives', config).then((response) => {
//       objectives_list.value = response.data;
//     });
//   };
//   return {
//     objectives_list, getObjectivesData
//   }
// }








