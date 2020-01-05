from . import data

def test_prof_skills_exist():
    for skills in data.PROF_SKILLS.values():
        for skill in skills:
            assert skill in data.SKILLS
