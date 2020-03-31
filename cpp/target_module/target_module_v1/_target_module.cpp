#include <Python.h>
#include <stdio.h>
#include <vector>
#include <array>
#include <map>
#include <string>

#include "Attributor.h"
#include "Attribution.h"
#include "enums.h"

using namespace std;

/* Docstrings */
static char module_docstring[] =
"This module provides an interface to calculate compute target startegy related things.";
static char targetsAttribution_docstring[] =
"";

/* Available functions */
static PyObject* targetsAttribution_target_module(PyObject* self, PyObject* args);

/* Module specification */
static PyMethodDef module_methods[] = {
	{ "targetsAttribution", targetsAttribution_target_module, METH_VARARGS, targetsAttribution_docstring },
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef moduledef = {
	PyModuleDef_HEAD_INIT,
	"_target_module",
	module_docstring,
	-1,
	module_methods,
	NULL,
	NULL,
	NULL,
	NULL,
};

/* Initialize the module */
PyMODINIT_FUNC PyInit__target_module(void)
{
	Py_Initialize();
	PyObject* module = PyModule_Create(&moduledef);
	if (module == NULL)
		return NULL;

	return module;
}

static PyObject* targetsAttribution_target_module(PyObject* self, PyObject* args)
{
	//receiving variables
	PyObject* units_list;
	PyObject* pItem;

	int n_units;
	int player_int;
	double timeout; // in seconds

	//output variables
	PyObject* ret;
	PyObject* py_all_attributions;
	PyObject* py_attributions;
	PyObject* py_vector;
	PyObject* py_attribution;

	

	/* Parse the input tuple */
	if (!PyArg_ParseTuple(args, "Oiid", &units_list, &n_units, &player_int, &timeout))
		return NULL;


	//variables conversion
	Creature player;
	map<Creature, vector<array<int, 3>>> creatures;

	for (int i = 0; i < n_units; i++)
	{
		pItem = PyList_GetItem(units_list, i);

		int x = (int)PyLong_AsLong(PyList_GetItem(pItem, 0));
		int y = (int)PyLong_AsLong(PyList_GetItem(pItem, 1));
		Creature creature;
		switch ((int)PyLong_AsLong(PyList_GetItem(pItem, 2)))
		{
		case 0:
			creature = Creature::Humans;
			break;
		case 1:
			creature = Creature::Us;
			break;
		case 2:
			creature = Creature::Them;
			break;

		}
		int number = (int)PyLong_AsLong(PyList_GetItem(pItem, 3));
		creatures[creature].push_back({ x, y, number });
	}


	switch (player_int)
	{
	case 1:
		player = Creature::Us;
		break;
	case 2:
		player = Creature::Them;
		break;
	}


	//computations
	Attributor attributor = Attributor(creatures, player, timeout);

	vector<Attributions> all_attributions = attributor.getTargetAttribution();
	Attribution empty_attribution = Attribution();

	//outputs construction
	int n_attributions = all_attributions.size();
	py_all_attributions = PyTuple_New(n_attributions); // all attributions
	for (int a = 0; a < n_attributions; a++)
	{
		py_attributions = PyTuple_New(2); //pair of vector of attributions
		for (int p = 0; p < 2; p++)
		{
			int n_elements;
			if (p == 0)
			{
				n_elements = (all_attributions[a].first).size();
			}
			else
			{
				n_elements = (all_attributions[a].second).size();
			}
			
			py_vector = PyTuple_New(n_elements);
			for (int e = 0; e < n_elements; e++) // each element of the vector
			{

				Attribution& attribution = empty_attribution;
				if (p == 0)
				{
					attribution = (all_attributions[a].first)[e];
				}
				else
				{
					attribution = (all_attributions[a].second)[e];
				}

				py_attribution = PyTuple_New(5);

				pItem = Py_BuildValue("i", attribution.start[0]);
				PyTuple_SET_ITEM(py_attribution, 0, pItem);

				pItem = Py_BuildValue("i", attribution.start[1]);
				PyTuple_SET_ITEM(py_attribution, 1, pItem);

				pItem = Py_BuildValue("i", attribution.target[0]);
				PyTuple_SET_ITEM(py_attribution, 2, pItem);

				pItem = Py_BuildValue("i", attribution.target[1]);
				PyTuple_SET_ITEM(py_attribution, 3, pItem);

				pItem = Py_BuildValue("i", attribution.number);
				PyTuple_SET_ITEM(py_attribution, 4, pItem);

				PyTuple_SET_ITEM(py_vector, e, py_attribution);
			}
			PyTuple_SET_ITEM(py_attributions, p, py_vector);
		}

		PyTuple_SET_ITEM(py_all_attributions, a, py_attributions);
	}

	ret = Py_BuildValue("O", py_all_attributions);

	return ret;
}