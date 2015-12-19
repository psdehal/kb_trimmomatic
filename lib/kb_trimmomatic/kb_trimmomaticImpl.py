#BEGIN_HEADER
import sys
import traceback
from biokbase.workspace.client import Workspace as workspaceService
#END_HEADER


class kb_trimmomatic:
    '''
    Module Name:
    kb_trimmomatic

    Module Description:
    A KBase module: kb_trimmomatic
This sample module contains one small method - filter_contigs.
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    #BEGIN_CLASS_HEADER
    workspaceURL = None
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        #END_CONSTRUCTOR
        pass

    def filter_contigs(self, ctx, params):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN filter_contigs
        
        print('Starting filter contigs method.')
        
        if 'workspace' not in params:
            raise ValueError('Parameter workspace is not set in input arguments')
        workspace_name = params['workspace']
        if 'contigset_id' not in params:
            raise ValueError('Parameter contigset_id is not set in input arguments')
        contigset_id = params['contigset_id']
        if 'min_length' not in params:
            raise ValueError('Parameter min_length is not set in input arguments')
        min_length_orig = params['min_length']
        min_length = None
        try:
            min_length = int(min_length_orig)
        except ValueError:
            raise ValueError('Cannot parse integer from min_length parameter (' + str(min_length_orig) + ')')
        if min_length < 0:
            raise ValueError('min_length parameter shouldn\'t be negative (' + str(min_length) + ')')
        
        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token) 
        try: 
            contigSet = wsClient.get_objects([{'ref': workspace_name+'/'+contigset_id}])[0]['data']
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            orig_error = ''.join('    ' + line for line in lines)
            raise ValueError('Error loading original ContigSet object from workspace:\n' + orig_error)
        provenance = ctx['provenance']
        
        print('Got ContigSet data.')
        
        # save the contigs to a new list
        good_contigs = []
        n_total = 0;
        n_remaining = 0;
        for contig in contigSet['contigs']:
            n_total += 1
            if len(contig['sequence']) >= min_length:
                good_contigs.append(contig)
                n_remaining += 1

        # replace the contigs in the contigSet object in local memory
        contigSet['contigs'] = good_contigs
        
        print('Filtered ContigSet to '+str(n_remaining)+' contigs out of '+str(n_total))
        
        # save the new object to the workspace
        obj_info_list = None
        try:
	        obj_info_list = wsClient.save_objects({
	                            'workspace':workspace_name,
	                            'objects': [
	                                {
	                                    'type':'KBaseGenomes.ContigSet',
	                                    'data':contigSet,
	                                    'name':contigset_id,
	                                    'provenance':provenance
	                                }
	                            ]
	                        })
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            orig_error = ''.join('    ' + line for line in lines)
            raise ValueError('Error saving filtered ContigSet object to workspace:\n' + orig_error)
        
        info = obj_info_list[0]

        print('saved:'+str(info))

        returnVal = {
                'new_contigset_ref': str(info[6]) + '/'+str(info[0])+'/'+str(info[4]),
                'n_initial_contigs':n_total,
                'n_contigs_removed':n_total-n_remaining,
                'n_contigs_remaining':n_remaining
            }
        
        print('returning:'+str(returnVal))
                
        #END filter_contigs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method filter_contigs return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def runTrimmomatic(self, ctx, input_params):
        # ctx is the context object
        # return variables are: report
        #BEGIN runTrimmomatic
        #END runTrimmomatic

        # At some point might do deeper type checking...
        if not isinstance(report, basestring):
            raise ValueError('Method runTrimmomatic return value ' +
                             'report is not type basestring as required.')
        # return the results
        return [report]
